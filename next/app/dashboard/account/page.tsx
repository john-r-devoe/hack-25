"use client";
import React, { JSX, useState } from 'react';
import {
  DragDropContext,
  Droppable,
  Draggable,
  DropResult,
} from "@hello-pangea/dnd";

// Helper function to reorder the priorities list.
const reorder = (list: string[], startIndex: number, endIndex: number): string[] => {
  const result = Array.from(list);
  const [removed] = result.splice(startIndex, 1);
  result.splice(endIndex, 0, removed);
  return result;
};

export default function AccountPage(): JSX.Element {
  // Initial priorities order.
  const initialPriorities = [
    "Foot Traffic",
    "Competitive Landscape",
    "Urban Density",
  ];
  const [priorities, setPriorities] = useState<string[]>(initialPriorities);
  const [hasChangedPriorities, setHasChangedPriorities] = useState(false);

  // Initial business description.
  const initialDescription = `The Starbucks located at 48 5th St NW, Atlanta, GA 30308, is a licensed café situated within the Barnes & Noble at Georgia Tech, right in the heart of Technology Square. This prime location makes it a convenient spot for Georgia Tech students, faculty, and visitors to enjoy a variety of Starbucks beverages and snacks. The café is directly across the street from the Georgia Tech Hotel and Conference Center, enhancing its accessibility for guests staying in the area.

Operating hours are Monday through Friday from 7:00 am to 6:00 pm, and the café is closed on weekends.`;
  const [description, setDescription] = useState(initialDescription);
  const [hasChangedDescription, setHasChangedDescription] = useState(false);

  // When drag ends, update the order.
  const onDragEnd = (result: DropResult) => {
    if (!result.destination) return;

    const newOrder = reorder(
      priorities,
      result.source.index,
      result.destination.index
    );
    setPriorities(newOrder);
    setHasChangedPriorities(
      JSON.stringify(newOrder) !== JSON.stringify(initialPriorities)
    );
  };

  const handleConfirmPriorities = () => {
    alert("Priorities confirmed: " + priorities.join(", "));
    setHasChangedPriorities(false);
  };

  const handleDescriptionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setDescription(e.target.value);
    setHasChangedDescription(e.target.value !== initialDescription);
  };

  const handleConfirmDescription = () => {
    alert("Business description confirmed!");
    setHasChangedDescription(false);
  };

  return (
    <div className="bg-white text-gray-700 h-full w-full p-8">
      {/* Name and Email Fields */}
      <div className="mb-6 space-y-4">
        <div>
          <label className="block mb-1 font-medium">Name:</label>
          <input
            type="text"
            className="border rounded w-full px-3 py-2"
            placeholder="Enter your name"
          />
        </div>
        <div>
          <label className="block mb-1 font-medium">Email:</label>
          <input
            type="email"
            className="border rounded w-full px-3 py-2"
            placeholder="Enter your email"
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
                  {priorities.map((priority, index) => (
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
          {/* Confirm Button for Priorities (centered) */}
          {hasChangedPriorities && (
            <button
              onClick={handleConfirmPriorities}
              className="bg-[#40798c] text-white rounded-lg py-2 px-4 mx-auto"
            >
              Confirm
            </button>
          )}
        </div>

        {/* Right Column: Business Description */}
        <div className="flex flex-col w-1/2 space-y-4">
          <h2 className="text-xl font-semibold">Edit business description</h2>
          <textarea
            className="border rounded w-full h-48 p-2 resize-none overflow-hidden"
            value={description}
            onChange={handleDescriptionChange}
          />
          {/* Confirm Button for Description (centered) */}
          {hasChangedDescription && (
            <button
              onClick={handleConfirmDescription}
              className="bg-[#40798c] text-white rounded-lg py-2 px-4 mx-auto"
            >
              Confirm
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
