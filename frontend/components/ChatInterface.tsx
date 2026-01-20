"use client";

import { useState, useRef, useEffect } from 'react';
import { Send, ArrowLeft } from 'lucide-react';
import { Message, Doctor } from '@/types';
import DoctorCard from './DoctorCard';
import Link from 'next/link';

export default function ChatInterface() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', role: 'ai', content: 'Hello! I can help you book an appointment. How can I help?', type: 'text' }
  ]);
  
  // Modal State
  const [selectedDoctor, setSelectedDoctor] = useState<Doctor | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMsg: Message = { id: Date.now().toString(), role: 'user', content: input, type: 'text' };
    setMessages(prev => [...prev, userMsg]);
    setInput('');

    // --- MOCK AI LOGIC (Simulating the Backend) ---
    setTimeout(() => {
      const lowerInput = userMsg.content.toLowerCase();

      // SCENARIO 1: User mentions "Dental" or "Teeth"
      if (lowerInput.includes('dental') || lowerInput.includes('teeth') || lowerInput.includes('tooth')) {
        
        // If they didn't specify time, pretend to ask (or just show suggestions)
        // For this demo, let's show the list directly as if they clicked a suggestion
        const response: Message = {
          id: Date.now().toString(),
          role: 'ai',
          content: "I found available dental specialists for today. Please select a slot:",
          type: 'doctor-list',
          data: [
            { id: '1', name: 'Dr. Smith', specialty: 'Dentist', hospital: 'City Care', timeSlot: '3:00 PM', experience: '10y', rating: 4.8 },
            { id: '2', name: 'Dr. Sarah', specialty: 'Orthodontist', hospital: 'Smile Clinic', timeSlot: '4:15 PM', experience: '5y', rating: 4.5 },
          ]
        };
        setMessages(prev => [...prev, response]);
      } 
      // SCENARIO 2: Default fallback
      else {
        setMessages(prev => [...prev, {
          id: Date.now().toString(),
          role: 'ai',
          content: "I can help with health issues. Try saying 'I need a dentist' or 'General checkup'.",
          type: 'text'
        }]);
      }
    }, 800);
  };

  return (
    <div className="flex flex-col h-screen bg-white">
      
      {/* Header */}
      <div className="p-4 border-b flex items-center gap-3">
        <Link href="/" className="p-2 hover:bg-gray-100 rounded-full">
          <ArrowLeft size={20} />
        </Link>
        <h1 className="font-semibold">Callex AI Agent</h1>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6 bg-gray-50">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white border text-gray-800'} p-3.5 rounded-2xl shadow-sm`}>
              <p className="leading-relaxed">{msg.content}</p>
              
              {/* If message has doctor data, render the horizontal list */}
              {msg.type === 'doctor-list' && msg.data && (
                <div className="mt-4 flex gap-3 overflow-x-auto pb-2 scrollbar-hide">
                  {msg.data.map(doc => (
                    <DoctorCard 
                      key={doc.id} 
                      doctor={doc} 
                      onBook={(d) => { setSelectedDoctor(d); setIsModalOpen(true); }} 
                    />
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white border-t">
        <div className="flex gap-2 max-w-3xl mx-auto">
          <input 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type 'I have dental issues'..."
            className="flex-1 px-5 py-3 bg-gray-100 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
          />
          <button onClick={handleSend} className="p-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors shadow-sm">
            <Send size={20} />
          </button>
        </div>
      </div>

      {/* CONFIRMATION MODAL */}
      {isModalOpen && selectedDoctor && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="bg-white rounded-2xl w-full max-w-sm p-6 shadow-2xl animate-in fade-in zoom-in duration-200">
            <h3 className="text-xl font-bold text-gray-900 mb-2">Confirm Booking</h3>
            <p className="text-gray-600 mb-6">
              You are booking <b>{selectedDoctor.name}</b> for <b>{selectedDoctor.timeSlot}</b> today.
            </p>
            <div className="flex gap-3">
              <button 
                onClick={() => setIsModalOpen(false)}
                className="flex-1 py-3 text-gray-700 font-medium hover:bg-gray-100 rounded-xl transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={() => { alert('Booked!'); setIsModalOpen(false); }}
                className="flex-1 py-3 bg-blue-600 text-white font-medium rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-200"
              >
                Confirm
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}