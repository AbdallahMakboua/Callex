import Link from 'next/link';
import { User, Calendar, MessageSquare } from 'lucide-react';

export default function Dashboard() {
  return (
    <main className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      
      {/* 1. Profile Section */}
      <div className="w-full max-w-md bg-white rounded-2xl shadow-sm p-6 mb-8 text-center border border-gray-100">
        <div className="w-20 h-20 bg-blue-100 rounded-full mx-auto flex items-center justify-center mb-4 text-blue-600">
          <User size={40} />
        </div>
        <h1 className="text-2xl font-bold text-gray-900">John Doe</h1>
        <p className="text-gray-500">Premium Member</p>
      </div>

      {/* 2. Action Buttons */}
      <div className="grid grid-cols-2 gap-4 w-full max-w-md">
        
        {/* Book Button -> Goes to Chat */}
        <Link href="/chat" className="group">
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:border-blue-500 hover:shadow-md transition-all cursor-pointer flex flex-col items-center gap-3">
            <div className="p-3 bg-blue-50 rounded-xl text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-colors">
              <MessageSquare size={32} />
            </div>
            <span className="font-semibold text-gray-700">Book Appt</span>
          </div>
        </Link>

        {/* Schedules Button (Placeholder) */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:border-purple-500 hover:shadow-md transition-all cursor-pointer flex flex-col items-center gap-3">
          <div className="p-3 bg-purple-50 rounded-xl text-purple-600">
            <Calendar size={32} />
          </div>
          <span className="font-semibold text-gray-700">My Schedules</span>
        </div>

      </div>
    </main>
  );
}