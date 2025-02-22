import { NextResponse } from "next/server";
import clientPromise from "../../../lib/mongodb";
import { NextApiRequest, NextApiResponse } from 'next';
export async function GET() {
    return NextResponse.json({
        hello: "world"
    });
}