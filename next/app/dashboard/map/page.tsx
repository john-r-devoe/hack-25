"use client";
import React, { JSX, useEffect, useState } from 'react';
import MyMapComponent from "./map.js";
import { redirect } from 'next/navigation.js';


export default function MapPage(): JSX.Element {
  const [center, setCenter] = useState({ lat: 40.7128, lng: -74.0060 });
  const [bounds, setBounds] = useState<google.maps.LatLngBounds | null>(null);
  const [zip, setZip] = useState("");
  const [analyzeDisabled, setAnalyzeDisabled] = useState<boolean>(false);

  useEffect(() => {
    setAnalyzeDisabled(!analyzeDisabled)
  }, [center])

  const handleSearch = (analyze:boolean) => {
    if (!zip) return;
    if (!window.google) {
      alert("Google Maps API not loaded yet.");
      return;
    }
    const geocoder = new window.google.maps.Geocoder();

    geocoder.geocode({ address: zip }, (results, status) => {
      if (status === "OK" && results && results[0]) {
        const location = results[0].geometry.location;
        setCenter({ lat: location.lat(), lng: location.lng() });
        if (analyze) {
          redirect("/dashboard/scores?address="+zip+"&lat="+location.lat()+"&lng="+location.lng())
        }
        if (results[0].geometry.bounds) {
          setBounds(results[0].geometry.bounds);
        } else if (results[0].geometry.viewport) {
          setBounds(results[0].geometry.viewport);
        } else {
          setBounds(null);
        }
      } else {
        alert("Geocode was not successful for the following reason: " + status);
      }
    });
  };

  return (
    <div className="relative h-screen">
      {/* Search Bar */}
      <div className="absolute top-4 left-1/2 z-20 w-full max-w-md -translate-x-1/2 transform">
        <div className="flex items-center space-x-2 rounded-md bg-white px-4 py-2 shadow-md">
          <input
            type="text"
            placeholder="Enter zip code or address"
            value={zip}
            onChange={(e) => setZip(e.target.value)}
            className="w-full border-none bg-transparent text-gray-700 outline-none placeholder:text-gray-400"
          />
          <button onClick={() => handleSearch(false)} className="px-4 py-2 bg-blue-500 text-white rounded transition duration-150 ease-in-out hover:scale-90">
            Search
          </button>
          <button onClick={() => handleSearch(true)} className={analyzeDisabled ? "px-4 py-2 bg-slate-600 text-white rounded" :"px-4 py-2 bg-green-500 text-white rounded transition duration-150 ease-in-out hover:scale-90" } disabled={analyzeDisabled}>
            Analyze
          </button>
        </div>
      </div>

      <MyMapComponent center={center} bounds={bounds} />
    </div>
  );
}
