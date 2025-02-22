import { UUID } from "mongodb"

export type NewUserDTO = 
| 
    {
        firstName: string,
        lastName: string,
        email: string,
        password: string,
        priorities: Array<string>
    }
| undefined

export type UserLocation = 
{
    address: string,
    index: number
}

export type User =
{
    userID: string,
    firstName: string,
    lastName: string,
    email: string,
    hashedPass: string,
    priorities: Array<string>,
    savedLocations: Array<UserLocation>
}

export type SessionPayload = 
{
    userID: string,
    expiresAt: Date
}