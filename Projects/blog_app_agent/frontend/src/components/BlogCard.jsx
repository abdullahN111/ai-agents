"use client";

import Image from "next/image";
import Link from "next/link";
import { FiCalendar, FiEye, FiArrowRight } from "react-icons/fi";
import { generateSlug } from "../utils/utils";

export default function BlogCard({ blog }) {
  const slug = generateSlug(blog.title);
  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  return (
    <div className="group flex flex-col bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 border border-gray-100 hover:-translate-y-1">
      <div className="relative h-56 w-full">
        <Image
          src={`${API_URL}/${blog.primary_image.replace("\\", "/")}`}
          alt={blog.title}
          fill
          className="object-cover group-hover:scale-105 transition-transform duration-300"
        />
        <div className="absolute top-4 left-4">
          <Link href={`/blogs/${blog.category.toLowerCase()}`}>
            <span className="px-3 py-1 bg-middle text-white text-sm font-semibold rounded-full shadow-md cursor-pointer">
              {blog.category}
            </span>
          </Link>
        </div>
      </div>

      <div className="flex flex-col flex-grow p-6">
        <h3 className="text-lg font-bold text-primary mb-2 line-clamp-2 group-hover:text-middle transition-colors">
          {blog.title}
        </h3>
        <p className="text-gray-600 mb-4 line-clamp-3 leading-relaxed text-sm">
          {blog.content}
        </p>

        <div className="flex items-center justify-between text-xs text-gray-500 mb-4 mt-auto">
          <div className="flex items-center">
            <FiCalendar className="mr-1.5" />
            <time dateTime={blog.created_at}>
              {new Date(blog.created_at).toLocaleDateString("en-US", {
                year: "numeric",
                month: "long",
                day: "numeric",
              })}
            </time>
          </div>
          <div className="flex items-center">
            <FiEye className="mr-1.5" />
            <span>300</span>
          </div>
        </div>

        <Link
          href={`/blogs/blog/${slug}`}
          className="inline-flex items-center justify-center px-4 py-2.5 bg-gray-100 text-primary text-sm font-semibold rounded-lg hover:bg-middle hover:text-white transition-all duration-300 group/btn"
        >
          Read Article
          <FiArrowRight className="ml-2 group-hover/btn:translate-x-1 transition-transform" />
        </Link>
      </div>
    </div>
  );
}
