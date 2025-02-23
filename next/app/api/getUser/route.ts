import { GetUserDTO } from "@/lib/definitions";
import clientPromise from "@/lib/mongodb";
import { NextRequest } from "next/server";

export async function GET(req:NextRequest) {
    console.log("GET USER HIT");

    const client = await clientPromise.connect();
    try {
        const searchParams = req.nextUrl.searchParams
        const data = searchParams.get('id')
        console.log("ENTRIES")
        console.log(searchParams.entries())
        if (!data) {
            throw new Error("Cannot GET with no id");
        }
        console.log(data)
        const db = await client.db("BizzIn");
        const users = await db.collection("users");
        
        const found = await users.findOne({userID: data});
        if (!found) {
            throw new Error("No user exists with that ID");
        }
        console.log("succesfully got");
        const toReturn:GetUserDTO = 
        {
            userID: found.userID,
            firstName: found.firstName,
            lastName: found.lastName,
            email: found.email,
            priorities: found.priorities,
            industry: found.industry,
            savedLocations: found.savedLocations
        }
        return new Response(JSON.stringify({message: "Success", obj: toReturn}), {
            status: 200
        });
        
    } catch (error) {
        console.error("Error parsing request body:", error);
        return new Response(JSON.stringify({ message: "Failure. Could not Get user" }), { status: 400 });
    }
}