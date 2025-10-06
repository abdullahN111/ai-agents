import { notFound } from "next/navigation";
import Image from "next/image";
import Link from "next/link";
import {
  FiCalendar,
  FiEye,
  FiArrowLeft,
  FiHeart,
  FiMessageSquare,
} from "react-icons/fi";
import BlogGrid from "../../../../components/BlogGrid";
import CommentForm from "../../../../components/CommentForm";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getBlog(slug) {
  const res = await fetch(`${API_URL}/blogs/${slug}`, { cache: "no-store" });
  if (!res.ok) return null;
  return res.json();
}

async function getRelatedBlogs(category, excludeId) {
  const res = await fetch(`${API_URL}/blogs/category/${category}`, {
    cache: "no-store",
  });
  if (!res.ok) return [];
  const blogs = await res.json();
  return blogs.filter((b) => b.id !== excludeId).slice(0, 2);
}

async function getComments(blogId) {
  const res = await fetch(`${API_URL}/blogs/${blogId}/comments`, {
    cache: "no-store",
  });
  if (!res.ok) return [];
  return res.json();
}

export default async function BlogPage({ params }) {
  const { title } = await params;
  const blog = await getBlog(title);

  if (!blog) return notFound();

  const relatedBlogs = await getRelatedBlogs(blog.category, blog.id);
  const comments = await getComments(blog.id);

  const firstPart = blog.content.substring(0, 1200);
  const secondPart = blog.content.substring(1200);

  return (
    <article className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-[1440px] mx-auto px-4 md:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <Link
            href="/blogs"
            className="inline-flex items-center text-middle hover:text-primary mb-4 transition-colors"
          >
            <FiArrowLeft className="mr-2" />
            Back to Blogs
          </Link>

          <header className="mb-8">
            <div className="relative h-80 w-full rounded-xl overflow-hidden mb-4">
              <Image
                src={`${API_URL}/${blog.primary_image.replace("\\", "/")}`}
                alt={blog.title}
                fill
                className="object-cover"
              />
              <div className="absolute top-4 left-4">
                <span className="px-3 py-1 bg-middle text-white text-sm font-semibold rounded-full shadow-md">
                  {blog.category}
                </span>
              </div>
            </div>

            <h1 className="text-4xl font-bold text-primary mb-4">
              {blog.title}
            </h1>

            <div className="flex flex-wrap items-center justify-between gap-4 text-gray-600">
              <div className="flex items-center">
                <FiCalendar className="mr-2" />
                <time dateTime={blog.created_at}>
                  {new Date(blog.created_at).toLocaleDateString("en-US", {
                    year: "numeric",
                    month: "long",
                    day: "numeric",
                  })}
                </time>
              </div>
              <div className="flex items-center">
                <FiEye className="mr-2" />
                <span>300 views</span>
              </div>
            </div>
          </header>

          <div className="prose max-w-none bg-white rounded-xl p-6 md:p-8 shadow-md">
            <div className="text-gray-700 leading-relaxed whitespace-pre-line">
              <p>{firstPart}</p>

              {blog.secondary_image && (
                <div className="my-8 rounded-xl overflow-hidden">
                  <Image
                    src={`${API_URL}/${blog.secondary_image.replace(
                      "\\",
                      "/"
                    )}`}
                    alt={`${blog.title} - Additional content`}
                    width={800}
                    height={400}
                    className="w-full h-auto object-cover rounded-xl"
                  />
                </div>
              )}

              <p>{secondPart}</p>
            </div>
          </div>
          <div className="mt-8 bg-white rounded-xl shadow-md p-6 md:p-8">
            <div className="flex items-center justify-between mb-6">
              <button className="flex items-center gap-2 text-gray-600 hover:text-red-500 transition-colors">
                <FiHeart className="w-5 h-5" />
                <span>Add to Favorites</span>
              </button>
            </div>

            <div>
              <h3 className="text-xl font-semibold text-primary mb-4">
                Comments
              </h3>

              <CommentForm blogId={blog.id} />

              <div className="space-y-4">
                {comments.length > 0 ? (
                  comments.map((c) => (
                    <div key={c.id} className="p-4 bg-gray-50 rounded-lg">
                      <p className="text-gray-800 font-medium">{c.user_name}</p>
                      <p className="text-gray-600 text-sm">{c.text}</p>
                    </div>
                  ))
                ) : (
                  <p className="text-gray-500 text-sm">
                    No comments yet. Be the first!
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="mt-8">
          <h2 className="text-2xl font-bold text-primary mb-6">
            Related Articles
          </h2>
          <BlogGrid blogs={relatedBlogs} />
        </div>
      </div>
    </article>
  );
}
