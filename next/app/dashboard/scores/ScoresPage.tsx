"use client"

import { GetUserDTO, UserLocation } from "@/lib/definitions";
import { useState } from "react";
import LocationItem from "./LocationItem";
import Image from "next/image";
import StreetView from "./StreetView";
import { useSearchParams } from 'next/navigation'

export default function ScoresPage({user}:{user:GetUserDTO}) {
    const [selectedLocation, setSelectedLocation] = useState<UserLocation|undefined>(undefined);
    const [selectedLocationSaved, setSelectedLocationSaved] = useState<boolean>(true);

    const locationSelected = (location:UserLocation) => {
        setSelectedLocation(location)
    }

    const locationDeleted = (location:UserLocation) => {
        //delete location from db
    }

    const searchParams = useSearchParams()
    const urlAddress = searchParams.get('address')
    if(urlAddress) {
        const saved = user.savedLocations.find((value) => {
            value.address == urlAddress
        })
        if (saved) {
            locationSelected(saved)
        } else {

        }
    }

    if (selectedLocation) {
        return (
            <div className="w-full h-fit flex flex-col flex-wrap p-14 bg-white gap-11">
                {/* Header */}
                <div className="w-full flex justify-between">
                    {/* Exit */}
                    <div className="flex w-fit gap-2 text-[#40798c] font-bold cursor-pointer transition duration-200 ease-in-out hover:scale-110" onClick={() => setSelectedLocation(undefined)}>
                        <span>&larr;</span>
                        <p>Exit to All Scores</p>
                    </div>
                    <h2 className="text-2xl font-extralight">{selectedLocation.address}</h2>
                    <button onClick={() => {
                            setSelectedLocation(undefined)
                            locationDeleted(selectedLocation)
                        }}>
                        <Image
                        src="/bookmark-svgrepo-filled-com.svg"
                        alt=""
                        width={25}
                        height={30}
                        className="transition delay-75 duration-300 ease-in-out hover:-translate-y-1 hover:scale-110"
                        />
                    </button>
                </div>
                {/* StreetView */}
                <StreetView latlng={selectedLocation.latlng}/>

                {/* Description */}
                <div className="flex flex-col align-middle justify-start w-full h-auto p-20 min-h-[900px] bg-[#f9fafb] rounded-2xl shadow-sm gap-7">
                    <h2 className="text-center text-4xl">Location score: <b>{selectedLocation.index}</b></h2>
                    <p>{selectedLocation.description ? selectedLocation.description : "Sorry, we couldn't find any information on this property!"}</p>
                </div>

            </div>
        )
        
    } else if (user.savedLocations.length > 0) {
        return (
            <div className="w-full h-full flex flex-row flex-wrap p-14 bg-white gap-6">
                {
                    user.savedLocations.map((location, index) => {
                        return <LocationItem location={location} locationSelected={locationSelected} locationDeleted={locationDeleted} key={location.address}/>
                    })
                }
            </div>
        )
    } else {
        return (
            <div className="flex h-full w-full bg-white text-gray-500">
                <div className="m-auto">
                    <h1 className="text-2xl">No Saved Scores Yet</h1>
                </div>
            </div>
        )
    }
}
