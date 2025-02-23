"use client";
import React, { JSX, useState } from 'react';
import Sidebar from "./map/sidebar";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps): JSX.Element {
  return (
    <div className="relative flex h-screen w-screen overflow-hidden">
      <Sidebar />
      <main className="relative flex-1 bg-[#40798c]">
        {children}
      </main>
    </div>
  );
}
