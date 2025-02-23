import { UUID } from "mongodb"

export type NewUserDTO = 
| 
    {
        firstName: string,
        lastName: string,
        email: string,
        password: string,
        priorities: Array<string>,
        industry: string
    }
| undefined

export type GetUserDTO =
{
    userID: string
    firstName: string,
    lastName: string,
    email: string,
    priorities: Array<string>,
    industry: string,
    savedLocations: Array<UserLocation>
}

export type UserLocation = 
{
    address: string,
    index?: number,
    latlng: Array<number>,
    description: string
}

export type User =
{
    userID: string,
    firstName: string,
    lastName: string,
    email: string,
    hashedPass: string,
    priorities: Array<string>,
    industry: string,
    savedLocations: Array<UserLocation>
}

export type SessionPayload = 
{
    userID: string,
    expiresAt: Date
}

export type ResponseData =
{
    message: string,
    obj?: {}
}

export type EmailPassDTO =
{
    email: string,
    password: string
}