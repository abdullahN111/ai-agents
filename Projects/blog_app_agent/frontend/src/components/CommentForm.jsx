"use client";

import { useSession } from "next-auth/react";
import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function CommentForm({ blogId }) {
  const { data: session } = useSession();
  console.log("Session data:", session);

  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!session) {
      setError("You must be logged in to comment");
      return;
    }

    if (!text.trim()) {
      setError("Comment cannot be empty");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/comments`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${session.id_token}`,
        },
        body: JSON.stringify({
          blog_id: Number(blogId),
          text: text.trim(),
        }),
        credentials: "include",
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(
          errorData.detail || `HTTP error! status: ${res.status}`
        );
      }

      setText("");
    } catch (err) {
      setError(err.message || "Failed to post comment");
      console.error("Comment submission error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6">
      <textarea
        rows={4}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Write a comment..."
        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:outline-none resize-none"
      ></textarea>

      {error && <div className="mt-2 text-red-600 text-sm">{error}</div>}

      <button
        type="submit"
        disabled={loading}
        className="mt-3 px-5 py-2 bg-primary text-white font-medium rounded-lg shadow hover:bg-middle transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? "Posting..." : "Post Comment"}
      </button>
    </form>
  );
}
