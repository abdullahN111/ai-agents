"use client";

import { useRef, useState } from "react";
import { FiArrowRight, FiBookOpen, FiCheck, FiLoader } from "react-icons/fi";
import { categories } from "../../../public/assets/blogRelatedData";

export default function CreateBlog() {
  const formRef = useRef(null)
  const [buttonState, setButtonState] = useState("idle");

  const [formData, setFormData] = useState({
    topic: "",
    views: "",
    popularity: "medium",
    category: "",
    primaryImage: null,
    secondaryImage: null,
  });

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (files) {
      setFormData((prev) => ({
        ...prev,
        [name]: files[0],
      }));
    } else {
      setFormData((prev) => ({
        ...prev,
        [name]: value,
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setButtonState("loading");
    try {
      const formDataToSend = new FormData();
      formDataToSend.append("primary_image", formData.primaryImage);
      formDataToSend.append("secondary_image", formData.secondaryImage);

      const uploadResponse = await fetch(
        "http://127.0.0.1:8000/upload-images",
        {
          method: "POST",
          body: formDataToSend,
        }
      );

      const imagePaths = await uploadResponse.json();
      const API_URL =
        process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const agentResponse = await fetch(`${API_URL}/agent`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          input: `Title: ${formData.topic}\nPerspective: ${formData.views}`,
        }),
      });

      const agentResult = await agentResponse.json();

      const blogResponse = await fetch("http://127.0.0.1:8000/blogs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: formData.topic,
          perspective: formData.views,
          category: formData.category,
          popularity: formData.popularity,
          primary_image: imagePaths.primary,
          secondary_image: imagePaths.secondary,
          content: agentResult.output.content,
        }),
      });

      if (blogResponse.ok) {
        console.log("Blog created successfully!");
        setButtonState("success");
        setTimeout(() => {
          setFormData({
            topic: "",
            views: "",
            popularity: "medium",
            category: "",
            primaryImage: null,
            secondaryImage: null,
          });
          if (formRef.current) {
            formRef.current.reset();
          }
          setButtonState("idle");
        }, 2000);
      } else {
        setButtonState("idle");
      }
    } catch (error) {
      console.error("Error creating blog:", error);
      setButtonState("idle");
    }
  };
  const getButtonContent = () => {
    switch (buttonState) {
      case "loading":
        return (
          <>
            <FiLoader className="animate-spin mr-2" />
            Generating...
          </>
        );
      case "success":
        return (
          <>
            <FiCheck className="mr-2" />
            Blog Generated!
          </>
        );
      default:
        return (
          <>
            Generate Blog
            <FiArrowRight className="ml-2" />
          </>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-higher rounded-full mb-4">
            <FiBookOpen className="w-8 h-8 text-blue-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Create New Blog Post
          </h1>
          <p className="text-lg text-gray-600">
            Provide the essential details to generate your blog content
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-higher overflow-hidden">
          <form onSubmit={handleSubmit} className="p-8">
            <div className="space-y-6">
              <div>
                <label
                  htmlFor="topic"
                  className="block text-sm font-medium text-primary mb-2"
                >
                  Blog Topic *
                </label>
                <input
                  type="text"
                  id="topic"
                  name="topic"
                  value={formData.topic}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border-higher border rounded-lg focus:outline-middle transition-colors"
                  placeholder="What is the main topic of your blog?"
                  required
                />
              </div>

              <div>
                <label
                  htmlFor="views"
                  className="block text-sm font-medium text-primary mb-2"
                >
                  Your Perspective *
                </label>
                <textarea
                  id="views"
                  name="views"
                  rows={4}
                  value={formData.views}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border-higher border rounded-lg focus:outline-middle transition-colors"
                  placeholder="Share your unique perspective or angle on this topic..."
                  required
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label
                    htmlFor="popularity"
                    className="block text-sm font-medium text-primary mb-2"
                  >
                    Topic Popularity
                  </label>
                  <select
                    id="popularity"
                    name="popularity"
                    value={formData.popularity}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border-higher border rounded-lg focus:outline-middle transition-colors"
                  >
                    <option value="low">Not very popular</option>
                    <option value="medium">Moderately popular</option>
                    <option value="high">Very popular</option>
                  </select>
                </div>

                <div>
                  <label
                    htmlFor="category"
                    className="block text-sm font-medium text-primary mb-2"
                  >
                    Category *
                  </label>
                  <select
                    id="category"
                    name="category"
                    value={formData.category}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border-higher border rounded-lg focus:outline-middle transition-colors"
                    required
                  >
                    <option value="">Select a category</option>
                    {categories.map((category) => (
                      <option key={category} value={category}>
                        {category}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label
                  htmlFor="primaryImage"
                  className="block text-sm font-medium text-primary mb-2"
                >
                  Primary Image *
                </label>
                <input
                  type="file"
                  id="primaryImage"
                  name="primaryImage"
                  accept="image/*"
                  onChange={handleChange}
                  className="w-full px-4 py-3 border-higher border rounded-lg focus:outline-middle transition-colors file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-middle file:text-white hover:file:bg-[#f31e65ef]"
                  required
                />
              </div>

              <div>
                <label
                  htmlFor="secondaryImage"
                  className="block text-sm font-medium text-primary mb-2"
                >
                  Secondary Image
                </label>
                <input
                  type="file"
                  id="secondaryImage"
                  name="secondaryImage"
                  accept="image/*"
                  onChange={handleChange}
                  className="w-full px-4 py-3 border-higher border rounded-lg focus:outline-middle transition-colors file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-middle file:text-white hover:file:bg-[#f31e65ef]"
                />
              </div>
            </div>

            <div className="mt-8 pt-6 border-t border-gray-200">
              <button
                type="submit"
                disabled={buttonState === "loading"}
                className={`w-full flex items-center justify-center px-6 py-3 text-white font-medium rounded-lg transition-all duration-300 cursor-pointer ${
                  buttonState === "loading"
                    ? "bg-gray-400"
                    : buttonState === "success"
                    ? "bg-green-500"
                    : "bg-middle hover:bg-[#f31e65ef] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#f31e65da]"
                }`}
              >
                {getButtonContent()}
              </button>
            </div>
          </form>
        </div>

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>
            Your blog will be automatically generated by our AI based on the
            information you provide.
          </p>
        </div>
      </div>
    </div>
  );
}
