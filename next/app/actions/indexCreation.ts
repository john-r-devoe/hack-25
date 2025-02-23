import { Preference } from "@/lib/definitions";

export default async function createIndex(address:string, industry:string, preferences:Preference) {
    console.log(address)
    console.log(industry)
    console.log(preferences)
    const result = await fetch("http://127.0.0.1:5000/createIndex", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({address: address, industry: industry, preferences: preferences})
    });
    return (await result.json())
}