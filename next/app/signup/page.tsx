"use client"

import { useState } from "react";
import { motion } from "framer-motion";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";
import { signup } from "../actions/authActions";
import { redirect } from "next/navigation";

export default function SignupPage() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
    industry: "clothing"
  });

  const [priorities, setPriorities] = useState([
    "Distance to Competition",
    "Foot-Traffic",
    "Urban Density"
  ]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.password == formData.confirmPassword) setStep(2);
    else {
        if (formData.password != formData.confirmPassword) {
            alert("Passwords don't match!")
        }
    }
  };

  const handleDragEnd = (result: any) => {
    if (!result.destination) return;
    const items = Array.from(priorities);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);
    setPriorities(items);
  };

  const  handleFinalSubmit = async () => {
    console.log(formData)
    const result = await signup({
        firstName: formData.firstName,
        lastName: formData.lastName,
        email: formData.email,
        password: formData.password,
        priorities: priorities,
        industry: formData.industry
    });
    alert(result?.obj);
    if(result?.message.includes("Success")) {
      redirect("/");
    } else if (result?.message.includes("already exists")) {
      alert("That email is already in use");
    }

  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#1F363D]">
      <motion.div 
        className="w-full max-w-md p-8 rounded-2xl shadow-lg bg-[#40798C]"
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5 }}
      >
        {step === 1 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-2xl font-bold text-center text-[#CFE0C3] mb-6">Sign Up</h2>
            <form className="space-y-4" onSubmit={handleFormSubmit}>
                <label className="block text-[#CFE0C3] mb-1">First Name</label>
                <input
                type="text"
                name="firstName"
                value={formData.firstName}
                onChange={handleChange}
                className="w-full p-2 rounded bg-[#70A9A1] text-[#1F363D] placeholder-[#9EC1A3] focus:outline-none focus:ring-2 focus:ring-[#9EC1A3]"
                required
                />

                <label className="block text-[#CFE0C3] mb-1">Last Name</label>
                <input
                type="text"
                name="lastName"
                value={formData.lastName}
                onChange={handleChange}
                className="w-full p-2 rounded bg-[#70A9A1] text-[#1F363D] placeholder-[#9EC1A3] focus:outline-none focus:ring-2 focus:ring-[#9EC1A3]"
                required
                  />

                <label className="block text-[#CFE0C3] mb-1">Email</label>
                <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="w-full p-2 rounded bg-[#70A9A1] text-[#1F363D] placeholder-[#9EC1A3] focus:outline-none focus:ring-2 focus:ring-[#9EC1A3]"
                required
                  />

                <label className="block text-[#CFE0C3] mb-1">Password</label>
                <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="w-full p-2 rounded bg-[#70A9A1] text-[#1F363D] placeholder-[#9EC1A3] focus:outline-none focus:ring-2 focus:ring-[#9EC1A3]"
                required
                  />

                <label className="block text-[#CFE0C3] mb-1">Confirm Password</label>
                <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className="w-full p-2 rounded bg-[#70A9A1] text-[#1F363D] placeholder-[#9EC1A3] focus:outline-none focus:ring-2 focus:ring-[#9EC1A3]"
                required
                  />


              <button
                type="submit"
                className="w-full p-2 mt-4 rounded bg-[#9EC1A3] text-[#1F363D] font-bold hover:bg-[#CFE0C3] transition"
              >
                Next
              </button>
            </form>
          </motion.div>
        )}

        {step === 2 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-2xl font-bold text-center text-[#CFE0C3] mb-6">Hello, {formData.firstName}</h2>
            <p className="text-center text-[#CFE0C3] mb-4">What's most important to you?</p>
            <DragDropContext onDragEnd={handleDragEnd}>
              <Droppable droppableId="priorities">
                {(provided) => (
                  <ul className="space-y-2" {...provided.droppableProps} ref={provided.innerRef}>
                    {priorities.map((item, index) => (
                      <Draggable key={item} draggableId={item} index={index}>
                        {(provided) => (
                          <li
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            className="p-2 bg-[#70A9A1] text-[#1F363D] text-center rounded cursor-move"
                          >
                            {item}
                          </li>
                        )}
                      </Draggable>
                    ))}
                    {provided.placeholder}
                  </ul>
                )}
              </Droppable>
            </DragDropContext>
            <button
              onClick={() => setStep(3)}
              className="w-full p-2 mt-4 rounded bg-[#9EC1A3] text-[#1F363D] font-bold hover:bg-[#CFE0C3] transition"
            >
              Next
            </button>
          </motion.div>
        )}

        {step == 3 && (
          <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          >

          <h2 className="text-2xl font-bold text-center text-[#CFE0C3] mb-6">Last Step!</h2>
          <p className="text-center text-[#CFE0C3] mb-4">What Industry are you in?</p>
          <form className="space-y-4">
              <select value={formData.industry}
              onChange={(e) => setFormData({...formData, industry: e.target.value})}
              className="w-full p-2 rounded bg-[#70A9A1] text-[#1F363D] placeholder-[#9EC1A3] focus:outline-none focus:ring-2 focus:ring-[#9EC1A3]">
                <option value="Clothing">Clothing</option>
                <option value="Restaurant">Restaurant</option>
                <option value="Financial Services">Financial Services</option>
                <option value="Tech">Tech</option>
                <option value="Merchandise">Merchandise</option>
              </select>
              <button
                type="submit"
                onClick={handleFinalSubmit}
                className="w-full p-2 mt-4 rounded bg-[#9EC1A3] text-[#1F363D] font-bold hover:bg-[#CFE0C3] transition"
              >
                Done!
              </button>
            </form>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}
