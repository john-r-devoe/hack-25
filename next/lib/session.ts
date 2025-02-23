"use server"
import { SessionPayload } from '@/lib/definitions'
import { cookies } from 'next/headers'
import { sealData, unsealData } from 'iron-session'
 
const secretKey = process.env.SESSION_SECRET
const encodedKey = new TextEncoder().encode(secretKey)
 
export async function encrypt(payload: SessionPayload) {
  const encryptedSession = sealData(payload, {
    password: encodedKey.toString(),
  });
  return encryptedSession;
}
 
export async function decrypt(session: string | undefined = ''):Promise<any> {
  return unsealData(session, {password: encodedKey.toString()});
}
 
export async function createSession(userID: string) {
  console.log("SESSION CREATING")
  const expiresAt = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
  const session = await encrypt({ userID, expiresAt });
  const cookieStore = await cookies();
 
  cookieStore.set('session', session, {
    httpOnly: true,
    secure: true,
    expires: expiresAt,
    sameSite: 'lax',
    path: '/',
  });
}

export async function deleteSession() {
  const cookieStore = await cookies();
  cookieStore.delete('session');
}