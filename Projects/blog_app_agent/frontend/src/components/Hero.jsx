"use client";

import Image from "next/image";
import Link from "next/link";
import heroImage from "../../public/assets/hero.png";
import { useSession } from "next-auth/react";

export default function Hero() {
  const { data: session } = useSession();

  const isAdmin =
    session?.user?.email === process.env.NEXT_PUBLIC_ADMIN_EMAIL ||
    session?.user?.email === process.env.NEXT_PUBLIC_MOD_EMAIL;

    
  return (
    <section className="relative bg-gradient-to-r from-blue-50 to-indigo-50 overflow-hidden">
      <div className="max-w-[1440px] mx-auto px-4 md:px-6 lg:px-8 py-12 md:py-24">
        <div className="flex flex-col md:flex-row items-center gap-8 md:gap-12">
          <div className="md:w-1/2 flex flex-col space-y-6 text-center md:text-left">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-primary leading-tight">
              Sharing My{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-secondary to-[#f81762]">
                Thoughts
              </span>{" "}
              With The World
            </h1>
            <p className="text-lg md:text-xl text-gray-600 max-w-lg mx-auto md:mx-0">
              Blogout is the platform I created to express my ideas, connect
              with readers, and build my online presence.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start mt-6">
              <Link
                href="mailto:myselfabdullah360@gmail.com"
                className="px-8 py-3 bg-primary text-white rounded-lg font-medium hover:bg-middle transition-colors shadow-md text-center"
              >
                Email Us
              </Link>
              {isAdmin && (
                <Link
                  href="/create-blog"
                  className="px-8 py-3 bg-white text-primary border border-primary rounded-lg font-medium hover:bg-gray-50 transition-colors text-center"
                >
                  Write Now
                </Link>
              )}
            </div>
          </div>

          <div className="md:w-1/2 flex justify-center relative">
            <div className="relative w-full max-w-md">
              <div className="absolute -inset-4 bg-gradient-to-r from-blue-200 to-indigo-200 rounded-3xl rotate-3 hidden md:block"></div>
              <div className="relative">
                <Image
                  src={heroImage}
                  alt="Young man wearing white shirt"
                  className="rounded-2xl object-contain w-full h-auto bg-higher"
                  priority
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
        <div className="absolute -top-20 -left-20 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div className="absolute -top-20 -right-20 w-72 h-72 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-20 left-20 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>
    </section>
  );
}
