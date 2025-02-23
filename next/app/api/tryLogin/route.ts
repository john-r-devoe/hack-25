import { NextRequest, NextResponse } from "next/server";
import clientPromise from "@/lib/mongodb";
import { EmailPassDTO } from "@/lib/definitions";
import bcrypt from "bcryptjs";
export async function GET(req:NextRequest) {
    console.log("GET LOGIN HIT");

    const client = await clientPromise.connect();
    try {
        const searchParams = req.nextUrl.searchParams
        const params = searchParams.get('cred')?.split('?')
        if (!params) {
            throw new Error("Data to GET cannot be undefined");
        }
        const email = params[0].trim()
        const password = params[1].trim()



        if (!email || !password) {
            throw new Error("Data to GET cannot be undefined");
        }
        const data:EmailPassDTO = {email:email, password:password};
        const db = await client.db("BizzIn");
        const users = await db.collection("users");
        
        const found = await users.findOne({email: data.email});
        if (!found || !bcrypt.compareSync(data.password, found.hashedPass)) {
            throw new Error("Invalid credentials");
        }
        console.log("FOUND");

        return new Response(JSON.stringify({message: "Success", obj: {userID: found.userID}}), {
            status: 200
        });
        
    } catch (error:any) {
        return new Response(JSON.stringify({ message: "Failure. " + error?.message }), { status: 400 });
    }
}