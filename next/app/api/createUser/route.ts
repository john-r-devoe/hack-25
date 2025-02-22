import { NewUserDTO, User } from "@/lib/definitions";
import { NextRequest, NextResponse } from "next/server";
import clientPromise from "@/lib/mongodb";
import { UUID } from "mongodb";
import { randomUUID } from "crypto";

export async function POST(req:NextRequest) {
    console.log("POST HIT");

    try {
        const body = await req.json();
        const data = body as NewUserDTO;
        if (!data) {
            throw new Error("Data to POST cannot be undefined");
        }
        const client = await clientPromise;
        const db = client.db("BizzIn");
        const users = db.collection("users");
        
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
            savedLocations: []
        }

        const result = await users.insertOne(newUser);
        if (result.acknowledged) {
            console.log("succesfully posted");
            await client.close();
            return new Response(JSON.stringify({message: "Success", addedObj: newUser}), {
                status: 200
            });
        } else {
            throw new Error("Something went wrong saving to the db");
        }
        
    } catch (error) {
        console.error("Error parsing request body:", error);
        return new Response(JSON.stringify({ error: "Could not POST" }), { status: 400 });
    }
}