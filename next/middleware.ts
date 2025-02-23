"use server"

import { NextRequest, NextResponse } from 'next/server'
import { decrypt } from '@/lib/session'
import { cookies } from 'next/headers'
 
// 1. Specify protected and public routes
const protectedRoutes = ['/dashboard', '/dashboard/account', '/dashboard/map', '/dashboard/scores']
const publicRoutes = ['/login', '/signup', '/']
 
export default async function middleware(req: NextRequest) {
  // 2. Check if the current route is protected or public
  const path = req.nextUrl.pathname
  const isProtectedRoute = protectedRoutes.includes(path)
  const isPublicRoute = publicRoutes.includes(path)
 
  // 3. Decrypt the session from the cookie
  const cookie = (await cookies()).get('session')?.value
  const session = await decrypt(cookie)
 
  // 4. Redirect to /login if the user is not authenticated
  if (isProtectedRoute && !session?.userID) {
    return NextResponse.redirect(new URL('/', req.nextUrl))
  }
 
  // 5. Redirect to /dashboard if the user is authenticated
  if (
    isPublicRoute &&
    session?.userID &&
    !req.nextUrl.pathname.startsWith('/dashboard')
  ) {
    return NextResponse.redirect(new URL('/dashboard/map', req.nextUrl))
  }

  if (
    isProtectedRoute &&
    session?.userID &&
    req.nextUrl.pathname == '/dashboard'
  ) {
    return NextResponse.redirect(new URL('/dashboard/map', req.nextUrl))
  }
 
  return NextResponse.next()
}