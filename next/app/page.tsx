"use client"

import Image from "next/image";
import { testDatabaseConnection } from "./actions";
import { useEffect, useState } from "react";

export default function Home() {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [testData, setTestData] = useState<object>([]);

  useEffect(() => {
    console.log(testData);
  }, [testData]);

  const tryLogin = async function (email:string|undefined, password:string|undefined):Promise<void> {
    if (!email || !password) {
      alert("Please enter a non-empty value for email and password.");
    }
    const response = await fetch("/api/tryLogin");
    if (response) {
      const data = await response.json();
      console.log(data);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#1F363D]">
      <div className="w-full max-w-md p-8 rounded-2xl shadow-lg bg-[#40798C]">
        <h2 className="text-2xl font-bold text-center text-[#CFE0C3] mb-6">BizzIn Login</h2>
        <form className="space-y-4">
          <div>
            <label className="block text-[#CFE0C3] mb-1">Email</label>
            <input
              type="email"
              className="w-full p-2 rounded bg-[#70A9A1] text-[#1F363D] placeholder-[#9EC1A3] focus:outline-none focus:ring-2 focus:ring-[#9EC1A3]"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-[#CFE0C3] mb-1">Password</label>
            <input
              type="password"
              className="w-full p-2 rounded bg-[#70A9A1] text-[#1F363D] placeholder-[#9EC1A3] focus:outline-none focus:ring-2 focus:ring-[#9EC1A3]"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button
            type="submit"
            className="w-full p-2 mt-4 rounded bg-[#9EC1A3] text-[#1F363D] font-bold hover:bg-[#CFE0C3] transition"
            onClick={(e) => {
              e.preventDefault();
              tryLogin(email, password);
            }}
          >
            Log In
          </button>
        </form>
        <p className="text-center text-[#CFE0C3] mt-4">
          Don't have an account? <a href="#" className="text-[#CFE0C3] font-bold hover:underline">Sign up</a>
        </p>
      </div>
    </div>
  );
}
