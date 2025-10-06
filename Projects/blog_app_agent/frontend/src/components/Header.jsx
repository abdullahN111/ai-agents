"use client";

import { useSession, signIn, signOut } from "next-auth/react";
import { useState, useRef, useEffect } from "react";
import Image from "next/image";
import Link from "next/link";
import logo from "../../public/assets/logo.png";
import { FiMenu, FiChevronDown, FiUser } from "react-icons/fi";
import { IoIosCreate } from "react-icons/io";
import { categories } from "../../public/assets/blogRelatedData";
import { generateSlug } from "../utils/utils";

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isMobileBlogsOpen, setIsMobileBlogsOpen] = useState(false);
  const [isAccountDropdownOpen, setIsAccountDropdownOpen] = useState(false);
  const { data: session } = useSession();
  const dropdownRef = useRef(null);

  const isAdmin =
    session?.user?.email === process.env.NEXT_PUBLIC_ADMIN_EMAIL ||
    session?.user?.email === process.env.NEXT_PUBLIC_MOD_EMAIL;

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const toggleMobileBlogs = () => {
    setIsMobileBlogsOpen(!isMobileBlogsOpen);
  };

  const toggleAccountDropdown = () => {
    setIsAccountDropdownOpen(!isAccountDropdownOpen);
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsAccountDropdownOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <header className="bg-white shadow-md relative">
      <nav className="max-w-[1440px] mx-auto flex items-center justify-between px-4 md:px-6 lg:px-8 py-1">
        <div className="flex items-center">
          <Link href="/" className="flex items-center">
            <Image src={logo} alt="Blogout Logo" width={75} height={75} />
            <span className="font-semibold text-[22px] sm:text-[23px] md:text-2xl text-primary">
              Blogout
            </span>
          </Link>
        </div>

        <ul className="hidden md:flex items-center gap-7 lg:gap-8">
          <li>
            <Link
              href="/"
              className="text-primary hover:text-middle transition-colors text-base md:text-[17px]"
            >
              Home
            </Link>
          </li>
          <li className="relative group">
            <button className="text-primary hover:text-middle transition-colors text-base md:text-[17px] flex items-center">
              Blogs
              <FiChevronDown className="transition-transform duration-200 group-hover:rotate-180" />
            </button>

            <div
              className={`
      absolute top-full left-0 mt-1 w-48 bg-white rounded-md shadow-lg py-2 z-50 border border-gray-200 
      opacity-0 scale-y-95 pointer-events-none
      group-hover:opacity-100 group-hover:scale-y-100 group-hover:pointer-events-auto
      transform origin-top transition-all duration-200 ease-in-out
    `}
            >
              {categories.map((category) => {
                const slug = generateSlug(category);
                return (
                  <Link
                    key={slug}
                    href={`/blogs/${slug}`}
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-middle hover:text-white transition-colors duration-200"
                  >
                    {category}
                  </Link>
                );
              })}
            </div>
          </li>

          <li>
            <Link
              href="/about"
              className="text-primary hover:text-middle transition-colors text-base md:text-[17px]"
            >
              About
            </Link>
          </li>
        </ul>

        <div className="hidden md:flex items-center gap-4">
          {isAdmin && (
            <>
              <Link
                href="/create-blog"
                className="text-middle transition-colors text-base md:text-[17px] hover:scale-110 duration-200"
              >
                <IoIosCreate size={32} />
              </Link>
            </>
          )}

          <div className="relative" ref={dropdownRef}>
            {session ? (
              <>
                {session.user?.image && (
                  <Image
                    onClick={toggleAccountDropdown}
                    src={session.user.image}
                    alt="User profile"
                    width={38}
                    height={38}
                    className="rounded-full cursor-pointer"
                    aria-label="Account"
                  />
                )}
              </>
            ) : (
              <button
                onClick={toggleAccountDropdown}
                className="text-middle transition-colors hover:scale-110 duration-200 cursor-pointer mt-2"
                aria-label="Account"
              >
                <FiUser size={28} />
              </button>
            )}

            <div
              className={`absolute right-0 top-full mt-2 w-64 bg-white rounded-md shadow-lg py-2 z-50 border border-gray-200
                transform origin-top transition-all duration-200 ease-out
                ${
                  isAccountDropdownOpen
                    ? "opacity-100 scale-100 pointer-events-auto"
                    : "opacity-0 scale-95 pointer-events-none"
                }`}
            >
              <div className="p-4">
                {session ? (
                  <div className="space-y-3">
                    <div className="flex items-center gap-3">
                      {session.user?.image && (
                        <Image
                          src={session.user.image}
                          alt="User profile"
                          width={40}
                          height={40}
                          className="rounded-full"
                        />
                      )}
                      <div>
                        <p className="font-semibold text-sm">
                          {session.user?.name}
                        </p>
                        <p className="text-gray-600 text-xs">
                          {session.user?.email}
                        </p>
                      </div>
                    </div>

                    <div className="pt-2 border-t border-gray-100">
                      <Link
                        href="/account"
                        className="block text-middle hover:text-middle-dark text-sm py-1 transition-colors duration-200"
                        onClick={() => setIsAccountDropdownOpen(false)}
                      >
                        Manage Account
                      </Link>
                    </div>

                    <button
                      onClick={() => signOut()}
                      className="w-full text-left text-red-600 hover:text-red-800 text-sm py-1 transition-colors duration-200 cursor-pointer"
                    >
                      Sign Out
                    </button>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <p className="text-gray-600 text-sm">
                      You are not signed in.
                    </p>
                    <button
                      onClick={() => signIn("google")}
                      className="w-full bg-middle text-white py-2 px-4 rounded-md hover:bg-middle-dark transition-colors duration-200 text-sm cursor-pointer"
                    >
                      Sign in with Google
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="md:hidden flex items-center gap-4">
          <button
            className="flex flex-col justify-center items-center w-10 h-10 py-[6px] rounded cursor-pointer"
            onClick={toggleMenu}
            aria-label="Toggle menu"
          >
            <FiMenu className="text-4xl" />
          </button>
        </div>
      </nav>

      <div
        className={`md:hidden fixed inset-0 bg-black opacity-0 z-40 transition-opacity duration-300 ease-in-out ${
          isMenuOpen ? "opacity-30" : "opacity-0 pointer-events-none"
        }`}
        onClick={toggleMenu}
      ></div>

      <div
        className={`md:hidden fixed top-0 right-0 h-full w-4/5 max-w-sm bg-white z-50 shadow-lg transform transition-transform duration-300 ease-in-out ${
          isMenuOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="p-5 sm:p-6 h-full flex flex-col">
          <div className="flex justify-end mb-6">
            <button
              onClick={toggleMenu}
              className="w-10 h-10 rounded-full flex items-center justify-center hover:bg-secondary/30 transition-colors duration-200"
              aria-label="Close menu"
            >
              <svg
                className="w-6 h-6 text-primary"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
          <div className="flex items-center mb-6 border-b pb-5 border-gray-500">
            <Link href="/" className="flex items-center">
              <Image src={logo} alt="Blogout Logo" width={70} height={70} />
              <span className="font-semibold text-xl sm:text-[22px] text-primary">
                Blogout
              </span>
            </Link>
          </div>

          <ul className="flex flex-col mb-12">
            <li>
              <Link
                href="/"
                className="text-primary hover:text-middle transition-colors text-[17px] block py-[6px]"
                onClick={toggleMenu}
              >
                Home
              </Link>
            </li>
            <li className="relative">
              <button
                onClick={toggleMobileBlogs}
                className="text-primary hover:text-middle transition-colors text-[17px] py-[6px] w-full text-left flex items-center justify-between"
              >
                Blogs
                <FiChevronDown
                  className={`transition-transform duration-200 ${
                    isMobileBlogsOpen ? "rotate-180" : ""
                  }`}
                />
              </button>

              <div
                className={`overflow-hidden transition-all duration-300 ease-in-out ${
                  isMobileBlogsOpen
                    ? "max-h-64 opacity-100"
                    : "max-h-0 opacity-0"
                }`}
              >
                <div className="pl-4 my-2 max-h-40 overflow-y-auto custom-scrollbar">
                  <ul className="space-y-[6px]">
                    {categories.map((category) => {
                      const slug = generateSlug(category);
                      return (
                        <li key={slug}>
                          <Link
                            href={`/blogs/${slug}`}
                            className="text-primary hover:text-middle transition-colors text-[16px] block py-1"
                            onClick={toggleMenu}
                          >
                            {category}
                          </Link>
                        </li>
                      );
                    })}
                  </ul>
                </div>
              </div>
            </li>
            <li>
              <Link
                href="/about"
                className="text-primary hover:text-middle transition-colors text-[17px] block py-[6px]"
                onClick={toggleMenu}
              >
                About
              </Link>
            </li>
          </ul>

          <div className="py-6 border-t border-gray-500">
            {isAdmin && (
              <Link
                href="/create-blog"
                className="text-middle transition-colors block hover:scale-105 duration-400 mb-8"
                onClick={toggleMenu}
              >
                <div className="flex items-center gap-1">
                  <IoIosCreate size={32} />
                  <span className="mt-1">Create Blog</span>
                </div>
              </Link>
            )}

            {session ? (
              <div className="space-y-2">
                <div className="flex items-center gap-3 mb-3">
                  {session.user?.image && (
                    <Image
                      src={session.user.image}
                      alt="User profile"
                      width={40}
                      height={40}
                      className="rounded-full"
                    />
                  )}
                  <div>
                    <p className="font-semibold text-sm">
                      {session.user?.name}
                    </p>
                    <p className="text-gray-600 text-xs">
                      {session.user?.email}
                    </p>
                  </div>
                </div>

                <Link
                  href="/account"
                  className="block text-middle hover:text-middle-dark text-sm py-1 transition-colors duration-200"
                  onClick={toggleMenu}
                >
                  Manage Account
                </Link>

                <button
                  onClick={() => signOut()}
                  className="text-red-600 hover:text-red-800 text-sm py-1 transition-colors duration-200"
                >
                  Sign Out
                </button>
              </div>
            ) : (
              <button
                onClick={() => signIn("google")}
                className="w-full bg-middle text-white py-2 px-4 rounded-md hover:bg-middle-dark transition-colors duration-200 text-sm cursor-pointer"
              >
                Sign in with Google
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
