"use client";
import React, { JSX, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import Image from 'next/image';
import { MapIcon, ChartBarIcon, UserCircleIcon } from '@heroicons/react/24/solid';

export default function Sidebar(): JSX.Element {
  const pathname = usePathname();
  console.log("Current pathname:", pathname);

  // Check if the current path starts with the provided path segment.
  const isActive = (path: string) => pathname?.startsWith(path);

  // Define icon color classes
  const activeIconClass = "text-[#40798c]";
  const inactiveIconClass = "text-white hover:text-[#40798c] transition-colors";

  return (
    <aside className="z-10 flex w-16 flex-col items-center py-4 shadow-md space-y-4 bg-gradient-to-b from-[#9ec1a3]/80 to-transparent">
      {/* Logo */}
      <div className="w-16 h-16">
        <Image src="/logo.png" alt="Logo" width={64} height={64} />
      </div>

      {/* Map Icon - navigates to /dashboard/map */}
      <Link href="/dashboard/map" legacyBehavior>
        <a className="p-2 rounded-full transition-colors">
          <MapIcon className={`h-9 w-9 ${isActive("/dashboard/map") ? activeIconClass : inactiveIconClass}`} />
        </a>
      </Link>

      {/* Scores Icon - navigates to /dashboard/scores */}
      <Link href="/dashboard/scores" legacyBehavior>
        <a className="p-2 rounded-full transition-colors">
          <ChartBarIcon className={`h-9 w-9 ${isActive("/dashboard/scores") ? activeIconClass : inactiveIconClass}`} />
        </a>
      </Link>

      {/* Account Icon - navigates to /dashboard/account */}
      <Link href="/dashboard/account" legacyBehavior>
        <a className="p-2 rounded-full transition-colors">
          <UserCircleIcon className={`h-9 w-9 ${isActive("/dashboard/account") ? activeIconClass : inactiveIconClass}`} />
        </a>
      </Link>
    </aside>
  );
}
