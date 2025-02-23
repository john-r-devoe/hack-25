import { UserLocation } from "@/lib/definitions";
import Image from "next/image";

export default function LocationItem({location, locationSelected, locationDeleted} : 
            {location:UserLocation, locationSelected: (location:UserLocation) => any, locationDeleted: (location:UserLocation) => any}) {

    let indexColor = "";
    let indexNum = -1

    if(location.index) {
        indexNum = location.index
        if (location.index >= 80) {
            indexColor = "text-green-600"
        } else if (location.index >= 60) {
            indexColor = "text-yellow-400"
        } else {
            indexColor = "text-red-800"
        }
    }

    return (
        <div className="cursor-pointer w-80 h-80 rounded-3xl flex flex-col pt-8 border border-solid shadow-lg transition duration-300 ease-in-out hover:shadow-transparent" key={location.address} 
            onClick={() => locationSelected(location)}>

            {/* Icons */}
            <div className="flex flex-row justify-between px-8">
                <button onClick={() => locationDeleted(location)}>
                    <Image
                    src="/bookmark-svgrepo-filled-com.svg"
                    alt=""
                    width={25}
                    height={30}
                    className="transition delay-75 duration-300 ease-in-out hover:-translate-y-1 hover:scale-110"
                    />
                </button>

                <button onClick={() => locationDeleted(location)}>
                    <Image
                    src="/trash-interface-svgrepo-com.svg"
                    alt=""
                    width={25}
                    height={30}
                    className="transition delay-75 duration-300 ease-in-out hover:-translate-y-1 hover:scale-110"
                    />
                </button>
            </div>
            {/* Score and Address */}
            <div className="flex flex-col gap-12 content-center items-center">
                <h3 className={"text-5xl font-mono font-extrabold " + indexColor}>{indexNum}</h3>
                <p className="w-24 h-auto text-base">{location.address}</p>
            </div>

        </div>
    )
}