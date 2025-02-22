import Image from "next/image";
import { testDatabaseConnection } from "./actions";

export default async function Home() {
  const isConnected = await testDatabaseConnection();
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <h1>Connected ? {isConnected ? "YES" : "NO"}</h1>
    </div>
  );
}
