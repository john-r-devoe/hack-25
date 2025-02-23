"use client";
import React, { JSX, useState } from 'react';
import {
  DragDropContext,
  Droppable,
  Draggable,
  DropResult,
} from "@hello-pangea/dnd";
import { GetUserDTO } from '@/lib/definitions';
import { useRouter } from 'next/navigation';


// Helper function to reorder the priorities list.
const reorder = (list: string[], startIndex: number, endIndex: number): string[] => {
  const result = Array.from(list);
  const [removed] = result.splice(startIndex, 1);
  result.splice(endIndex, 0, removed);
  return result;
};

export default function AccountPage({user} : {user:GetUserDTO}): JSX.Element {
  const router = useRouter();
  const [changedUser, setChangedUser] = useState<GetUserDTO>(user)

  // When drag ends, update the order.
  const onDragEnd = (result: DropResult) => {
    if (!result.destination) return;

    const newOrder = reorder(
      changedUser.priorities ? changedUser.priorities : [],
      result.source.index,
      result.destination.index
    );
    setChangedUser({...changedUser, priorities: newOrder})
  };

  const confirmChanges = async () => {
    const result = await fetch("/api/patchUser?id=" + user.userID, {
      method: "PATCH",
      headers: {
        "Content-Type": "applications/json"
    },
    body: JSON.stringify(changedUser)
    });
    if (result.ok) {
      alert("Changes Saved")
      window.location.reload()
    }
  };

  
  return (
    <div className="bg-white text-gray-700 h-full w-full p-8">
      {/* Name and Email Fields */}
      <div className="mb-6 space-y-4">
        <div>
          <label className="block mb-1 font-medium">First Name:</label>
          <input
            type="text"
            className="border rounded w-full px-3 py-2"
            placeholder="Enter your name"
            value={changedUser.firstName}
            onChange={(e) => setChangedUser({...changedUser, firstName: e.target.value})}
          />
        </div>
        <div>
          <label className="block mb-1 font-medium">Last Name:</label>
          <input
            type="text"
            className="border rounded w-full px-3 py-2"
            placeholder="Enter your name"
            value={changedUser.lastName}
            onChange={(e) => setChangedUser({...changedUser, lastName: e.target.value})}
          />
        </div>
        <div>
          <label className="block mb-1 font-medium">Email:</label>
          <input
            type="email"
            className="border rounded w-full px-3 py-2"
            placeholder="Enter your email"
            value={changedUser.email}
            onChange={(e) => setChangedUser({...changedUser, email: e.target.value})}
          />
        </div>
      </div>

      {/* Two-column layout for Priorities and Business Description */}
      <div className="flex flex-1 space-x-8">
        {/* Left Column: Drag-and-Drop Priorities */}
        <div className="flex flex-col w-1/2 space-y-4">
          <h2 className="text-xl font-semibold">Edit your priorities</h2>
          <DragDropContext onDragEnd={onDragEnd}>
            <Droppable droppableId="priorities">
              {(provided) => (
                <div
                  {...provided.droppableProps}
                  ref={provided.innerRef}
                  className="space-y-2"
                >
                  {changedUser.priorities?.map((priority, index) => (
                    <Draggable
                      key={priority}
                      draggableId={priority}
                      index={index}
                    >
                      {(provided, snapshot) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                          className={`bg-[#9ec1a3] rounded-full text-white py-2 px-4 text-center ${
                            snapshot.isDragging ? "opacity-75" : ""
                          }`}
                        >
                          {priority}
                        </div>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </div>
              )}
            </Droppable>
          </DragDropContext>
        </div>

        {/* Right Column: Business Description */}
        <div className="flex flex-col w-1/2 space-y-4">
          <h2 className="text-xl font-semibold">Edit Industry</h2>
          <select value={changedUser.industry}
              onChange={(e) => {
                setChangedUser({...changedUser, industry: e.target.value})
              }}
              className="border rounded w-40 h-10 p-2 resize-none overflow-hidden">
                <option value="Clothing">Clothing</option>
                <option value="Restaurant">Restaurant</option>
                <option value="Financial Services">Financial Services</option>
                <option value="Tech">Tech</option>
                <option value="Merchandise">Merchandise</option>
              </select>
        </div>
      </div>
        {user != changedUser ? 
        <div>
        <button
                onClick={confirmChanges}
                className="bg-[#40798c] text-white rounded-lg py-2 px-4 mx-auto mt-40"
              >
                 Confirm Changes
              </button>
        </div> :
        ""
      }
      
    </div>
  );
}
