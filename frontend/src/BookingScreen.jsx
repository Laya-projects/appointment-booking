import { useEffect, useState } from "react";
import { getSlots, bookSlot } from "./api";

function BookingScreen({ patientName }) {
    const [slots, setSlots] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [bookingId, setBookingId] = useState(null);
    const [message, setMessage] = useState(null);

    const loadSlots = () => {
        setLoading(true);
        getSlots()
            .then((res) => setSlots(res.data))
            .catch(() => setError("Couldn't load available slots. Please try again."))
            .finally(() => setLoading(false));
    };

    useEffect(() => {
        loadSlots();
    }, []);

    const handleBook = async (slotId) => {
        if (!patientName.trim()) {
            setMessage({ type: "error", text: "Please enter your name before booking." });
            return;
        }
        setBookingId(slotId);
        setMessage(null);
        try {
            await bookSlot(slotId, patientName.trim());
            setMessage({ type: "success", text: "Appointment booked successfully!" });
            loadSlots();
        } catch (err) {
            if (err.response?.status === 409) {
                setMessage({ type: "error", text: "Sorry, that slot was just booked by someone else." });
                loadSlots();
            } else {
                setMessage({ type: "error", text: "Booking failed. Please try again." });
            }
        } finally {
            setBookingId(null);
        }
    };

    if (loading) return <div className="status">Loading available slots...</div>;
    if (error) return <div className="status error">{error}</div>;

    return (
        <div>
            {message && <div className={`banner ${message.type}`}>{message.text}</div>}

            {slots.length === 0 ? (
                <div className="status">No slots available right now.</div>
            ) : (
                <div className="slot-list">
                    {slots.map((slot) => (
                        <div key={slot.id} className="slot-card">
                            <div>
                                <strong>{slot.doctor_name}</strong> — {slot.specialization}
                            </div>
                            <div>
                                {new Date(slot.start_time).toLocaleString()} –{" "}
                                {new Date(slot.end_time).toLocaleTimeString()}
                            </div>
                            <button onClick={() => handleBook(slot.id)} disabled={bookingId === slot.id}>
                                {bookingId === slot.id ? "Booking..." : "Book"}
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default BookingScreen;

