import { NewUserDTO, User } from "@/lib/definitions";
import { NextRequest, NextResponse } from "next/server";
import clientPromise from "@/lib/mongodb";
import { randomUUID } from "crypto";

export async function POST(req:NextRequest) {
    console.log("POST NEW USER HIT");

    const client = await clientPromise.connect();
    try {
        const body = await req.json();
        const data = body as NewUserDTO;
        if (!data) {
            throw new Error("Data to POST cannot be undefined");
        }
        const db = await client.db("BizzIn");
        const users = await db.collection("users");
        
        const found = await users.findOne({email: data.email});
        if (found) {
            throw new Error("A user with that email already exists");
        }

        const uniqueID = randomUUID();
        const newUser:User = {
            userID: uniqueID,
            firstName: data.firstName,
            lastName: data.lastName,
            email: data.email,
            hashedPass: data.password,
            priorities: data.priorities,
            industry: data.industry,
            savedLocations: []
        }

        const result = await users.insertOne(newUser);
        if (result.acknowledged) {
            console.log("succesfully posted");
            return new Response(JSON.stringify({message: "Success", obj: newUser}), {
                status: 200
            });
        } else {
            throw new Error("Something went wrong saving to the db");
        }
        
    } catch (error) {
        console.error("Error parsing request body:", error);
        return new Response(JSON.stringify({ message: "Failure. Could not Post" }), { status: 400 });
    }
}