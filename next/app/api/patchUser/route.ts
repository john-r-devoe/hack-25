import { GetUserDTO } from "@/lib/definitions";
import clientPromise from "@/lib/mongodb";
import { NextRequest } from "next/server";

export async function PATCH(req:NextRequest) {
    console.log("PATCH USER HIT");

    const client = await clientPromise.connect();
    try {
        const searchParams = req.nextUrl.searchParams
        const id = searchParams.get('id')
        if (!id) {
            throw new Error("Cannot PATCH with no id");
        }
        const body = await req.json();
        const data = body as GetUserDTO;
        if (!data) {
            throw new Error("Update data cannot be undefined");
        }
        const db = await client.db("BizzIn");
        const users = await db.collection("users");
        
        const found =  users.findOne({userID: id});
        if (!found) {
            throw new Error("No user exists with that ID");
        }
        console.log("succesfully patching");
        users.replaceOne(found, data)
        
        return new Response(JSON.stringify({message: "Success", obj: data}), {
            status: 200
        });
        
    } catch (error) {
        console.error("Error parsing request body:", error);
        return new Response(JSON.stringify({ message: "Failure. Could not Get user" }), { status: 400 });
    }
}