import { NextRequest} from "next/server";
import clientPromise from "@/lib/mongodb";
import { UserLocation } from "@/lib/definitions";

export async function DELETE(req:NextRequest) {
    console.log("POST NEW LOCATION HIT");

    const client = await clientPromise.connect();
    try {
        const body = await req.json();
        const data = body as UserLocation;
        if (!data) {
            throw new Error("Data to POST cannot be undefined");
        }
        const searchParams = req.nextUrl.searchParams
        const id = searchParams.get('id')
        if (!id) {
            throw new Error("Cannot DELETE with no id");
        }
        const db = await client.db("BizzIn");
        const users = await db.collection("users");
        
        const found = await users.findOne({userID: id});
        if (!found) {
            throw new Error("Invalid userID");
        }
        const removed = found.savedLocations.filter((e:UserLocation) => e.address !== data.address)
        console.log("TEST DELETE")
        console.log(found.savedLocations)
        console.log("REMOVED")
        console.log(removed)

        const result = await users.replaceOne(found, {...found, savedLocations: removed})

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