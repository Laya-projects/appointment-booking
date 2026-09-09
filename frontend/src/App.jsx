import { useState } from "react";
import BookingScreen from "./BookingScreen";
import Appointments from "./Appointments";
import "./App.css";

function App() {
  const [tab, setTab] = useState("book"); // "book" | "appointments"
  const [patientName, setPatientName] = useState("");

  return (
    <div className="container">
      <h1>Appointment Booking</h1>

      <input
        type="text"
        placeholder="Enter your name"
        value={patientName}
        onChange={(e) => setPatientName(e.target.value)}
        className="name-input"
      />

      <div className="tabs">
        <button
          className={tab === "book" ? "tab active" : "tab"}
          onClick={() => setTab("book")}
        >
          Book Appointment
        </button>
        <button
          className={tab === "appointments" ? "tab active" : "tab"}
          onClick={() => setTab("appointments")}
        >
          My Appointments
        </button>
      </div>

      {tab === "book" ? (
        <BookingScreen patientName={patientName} />
      ) : (
        <Appointments patientName={patientName} />
      )}
    </div>
  );
}

export default App;