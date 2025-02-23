"use client"

import { GetUserDTO, Preference, UserLocation } from "@/lib/definitions";
import { useEffect, useState } from "react";
import LocationItem from "./LocationItem";
import Image from "next/image";
import StreetView from "./StreetView";
import { redirect, useSearchParams } from 'next/navigation'
import createIndex from "@/app/actions/indexCreation";

export default function ScoresPage({user}:{user:GetUserDTO}) {
    const [selectedLocation, setSelectedLocation] = useState<UserLocation|undefined>(undefined);
    const [selectedLocationSaved, setSelectedLocationSaved] = useState<boolean>(true);
    const [dataRecieved, setDataRecieved] = useState<boolean>(false);

    useEffect(() => {
        setSelectedLocationSaved(true)
    }, [])

    const locationSelected = (location:UserLocation) => {
        setSelectedLocation(location)
    }

    const locationDeleted = async (location:UserLocation) => {
        console.log(location)
        const data = await fetch("/api/deleteLocation?id=" + user.userID, {
            headers: {
                "Content-Type": "applications/json"
            },
            method: "DELETE",
            body: JSON.stringify(location)
        })
        if (!(await data.ok)) {
            alert("something went wrong saving to the database...")
        }
        redirect("/dashboard/scores")
    }

    const handleBookmark = async () => {
        if (!selectedLocationSaved) {
            const data = await fetch("/api/createLocation?id=" + user.userID, {
                headers: {
                    "Content-Type": "applications/json"
                },
                method: "POST",
                body: JSON.stringify(selectedLocation)
            })
            if (!(await data.ok)) {
                alert("something went wrong saving to the database...")
            }
        } else {
            if(selectedLocation) {
                locationDeleted(selectedLocation)
            }
        }
        setSelectedLocationSaved(!selectedLocationSaved)
    }

    const searchParams = useSearchParams()
    const urlAddress = searchParams.get('address')
    const lat = Number(searchParams.get('lat'))
    const lng = Number(searchParams.get('lng'))
    if(urlAddress && lat && lng && !dataRecieved) {
        setDataRecieved(true)
        const saved = user.savedLocations.find((value) => {
            value.address == urlAddress
        })
        if (saved) {
            locationSelected(saved)
        } else {
            const getIndex = async () => {
                const textPref = user.priorities;
                let inputPref:Preference = Preference.FPD;
                if (textPref[0].startsWith("F") && textPref[1].startsWith("P") && textPref[2].startsWith("D")) {
                    inputPref = Preference.FPD
                } else if (textPref[0].startsWith("P") && textPref[1].startsWith("D") && textPref[2].startsWith("F")) {
                    inputPref = Preference.PDF
                } else if (textPref[0].startsWith("F") && textPref[1].startsWith("D") && textPref[2].startsWith("P")) {
                    inputPref = Preference.FDP
                } else if (textPref[0].startsWith("P") && textPref[1].startsWith("F") && textPref[2].startsWith("D")) {
                    inputPref = Preference.PFD
                } else if (textPref[0].startsWith("D") && textPref[1].startsWith("F") && textPref[2].startsWith("P")) {
                    inputPref = Preference.DFP
                } else if (textPref[0].startsWith("D") && textPref[1].startsWith("P") && textPref[2].startsWith("F")) {
                    inputPref = Preference.DPF
                }
                const data = await createIndex(urlAddress, user.industry, inputPref)
                console.log(data)
                const items = data.items
                const location:UserLocation = {
                    address: urlAddress,
                    index: items.score,
                    latlng: [lat, lng],
                    description: items.description

                }
                setSelectedLocation(location)
                setSelectedLocationSaved(false)
            }
            getIndex()
        }
    }

    if (selectedLocation) {
        return (
            <div className="w-full h-auto flex flex-col flex-wrap p-14 bg-white gap-11">
                {/* Header */}
                <div className="w-full flex justify-between">
                    {/* Exit */}
                    <div className="flex w-fit gap-2 text-[#40798c] font-bold cursor-pointer transition duration-200 ease-in-out hover:scale-110" onClick={() => {
                        setSelectedLocation(undefined)
                        redirect("/dashboard/scores")
                        }}>
                        <span>&larr;</span>
                        <p>Exit to All Scores</p>
                    </div>
                    <h2 className="text-2xl font-extralight">{selectedLocation.address}</h2>
                    <button onClick={() => handleBookmark()}>
                        <Image
                        src={selectedLocationSaved ? "/bookmark-svgrepo-filled-com.svg" : "/bookmark-shapes-svgrepo-com.svg"}
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
                <div className="flex flex-col align-middle justify-start w-full h-fit p-20 bg-[#f9fafb] rounded-2xl shadow-sm gap-7 scroll-m-12 overflow-y-auto">
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
