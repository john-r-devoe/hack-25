"use server"
import { SignJWT, jwtVerify } from 'jose'
import { SessionPayload } from '@/lib/definitions'
import { cookies } from 'next/headers'
 
const secretKey = process.env.SESSION_SECRET
const encodedKey = new TextEncoder().encode(secretKey)
 
export async function encrypt(payload: SessionPayload) {
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw',
    encoder.encode(secretKey),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );

  const encodedPayload = encoder.encode(JSON.stringify(payload));
  const signature = await crypto.subtle.sign('HMAC', key, encodedPayload);
  return `${btoa(JSON.stringify(payload))}.${btoa(String.fromCharCode(...new Uint8Array(signature)))}`;
}

export async function decrypt(session: string | undefined = '') {
  try {
    const [encodedPayload] = session.split('.');
    return JSON.parse(atob(encodedPayload));
  } catch (error) {
    console.log('Failed to verify session');
  }
}
 
export async function createSession(userID: string) {
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