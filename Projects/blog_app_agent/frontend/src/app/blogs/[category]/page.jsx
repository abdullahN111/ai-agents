import BlogGrid from "../../../components/BlogGrid";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";


async function getBlogsByCategory(category) {
  const res = await fetch(`${API_URL}/blogs/category/${category}`, {
    cache: "no-store",
  });

  if (!res.ok) return [];

  return res.json();
}

export default async function CategoryPage({ params }) {
  const { category } = await params;
  const filteredBlogs = await getBlogsByCategory(category);

  return (
    <section className="py-16">
      <div className="max-w-[1440px] mx-auto px-3 md:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-primary mb-10 capitalize">
          {category} Blogs
        </h2>
        <BlogGrid blogs={filteredBlogs} />
      </div>
    </section>
  );
}
