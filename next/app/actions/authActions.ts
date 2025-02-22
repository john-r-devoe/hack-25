import { NewUserDTO } from "@/lib/definitions";
import { createSession } from "@/lib/session";
import {hash} from "bcryptjs";
import { redirect } from "next/navigation";

export async function signup(profileData: NewUserDTO):Promise<undefined | object> {
    if (!profileData) {
        throw Error("No profile inputted to submit");
    }
    const hashedPassword = await hash(profileData.password, 10);
    profileData.password = hashedPassword;
    let response = undefined;
    try{
        response = await fetch("/api/createUser", {
            method: "POST",
            headers: {
                "Content-Type": "applications/json"
            },
            body: JSON.stringify(profileData)
        });
        const responseData = await response.json();
        await createSession(responseData.addedObj.userID);
        // 5. Redirect user
        redirect('/dashboard');

    } catch(e) {
        console.error(e);
    }
    return response?.json();
}