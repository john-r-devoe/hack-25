import { cookies } from 'next/headers';
import { decrypt } from '@/lib/session';
import { redirect } from 'next/navigation';
import { cache } from 'react';

export const verifySession = cache(async () => {
    const cookie = (await cookies()).get('session')?.value;
    const session = await decrypt(cookie);

   
    if (!session?.userID) {
      redirect('/');
    }
   
    return { isAuth: true, userID: session.userID }
  })