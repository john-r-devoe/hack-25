import React, { JSX } from 'react';
import { verifySession } from '@/lib/dal';
import { GetUserDTO } from '@/lib/definitions';
import ScoresPage from './ScoresPage';

export default async function Page(): Promise<JSX.Element> {
    let user = undefined;
    const authorized = await verifySession();
    if (authorized.isAuth && !user) {
      const response = await fetch(process.env.URL+"/api/getUser?id="+ authorized.userID)
      let data = (await response.json())
      console.log(data)
      user = data.obj as GetUserDTO
    }
    if(user) {
      return <ScoresPage user={user} />
    } else {
      return <div></div>
    }
  }
