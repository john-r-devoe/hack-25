import { NewUserDTO, ResponseData } from "@/lib/definitions";
import { createSession } from "@/lib/session";
import {hash} from "bcryptjs";
import { redirect } from "next/navigation";

export async function signup(profileData: NewUserDTO):Promise<undefined | ResponseData> {
    if (!profileData) {
        throw Error("No profile inputted to submit");
    }
    const hashedPassword = await hash(profileData.password, 10);
    profileData.password = hashedPassword;
    let response = undefined;
    let responseData = undefined;
    console.log(profileData)
    try{
        response = await fetch("/api/createUser", {
            method: "POST",
            headers: {
                "Content-Type": "applications/json"
            },
            body: JSON.stringify(profileData)
        });
        responseData = await response.json();
        alert(responseData.message)
        if (responseData.message.includes("Success")){
            alert("REACHED CREATE SESSION")
            await createSession(responseData.obj.userID);
            return responseData;
        }
        return responseData;
        

    } catch(e) {
        console.error(e);
        return responseData;
    }
}

export async function login(email:string, password:string):Promise<undefined | ResponseData> {
    let response = undefined;
    let responseData = undefined;
    console.log(email)
    try {
        response = await fetch("/api/tryLogin?cred=" + email + "?" + password, {
            method: "GET",
        });
        responseData =  await response.json();
        if (responseData.message.includes("Success")){
            await createSession(responseData.obj.userID);
            return responseData;
        }
        return responseData;
    } catch(e) {
        console.error(e);
        return responseData;
    }
}