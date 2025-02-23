import { NextRequest} from "next/server";
import clientPromise from "@/lib/mongodb";

export async function POST(req:NextRequest) {
    console.log("POST NEW LOCATION HIT");

    const client = await clientPromise.connect();
    try {
        const body = await req.json();
        const data = body as Location;
        if (!data) {
            throw new Error("Data to POST cannot be undefined");
        }
        const searchParams = req.nextUrl.searchParams
        const id = searchParams.get('id')
        if (!id) {
            throw new Error("Cannot PATCH with no id");
        }
        const db = await client.db("BizzIn");
        const users = await db.collection("users");
        
        const found = await users.findOne({userID: id});
        if (!found) {
            throw new Error("Invalid userID");
        }

        const result = await users.replaceOne(found, {...found, savedLocations: [...found.savedLocations, data]})

        if (result.acknowledged) {
            console.log("succesfully posted");
            return new Response(JSON.stringify({message: "Success", obj: data}), {
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