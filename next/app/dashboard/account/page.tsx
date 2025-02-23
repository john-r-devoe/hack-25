import { verifySession } from '@/lib/dal';
import AccountPage from './AccountPage';
import { JSX } from 'react';
import { GetUserDTO } from '@/lib/definitions';




export default async function Home(): Promise<JSX.Element>   {
  let user = undefined;
  const authorized = await verifySession();
  if (authorized.isAuth) {
    const response = await fetch(process.env.URL+"/api/getUser?id="+ authorized.userID)
    let data = (await response.json())
    console.log(data)
    user = data.obj as GetUserDTO
  }
  if(user) {
    return <AccountPage user={user} />
  } else {
    return <div></div>
  }
}
