"use client";

import Link from "next/link";
import Image from "next/image";
import { FaLinkedin, FaInstagram, FaEnvelope } from "react-icons/fa";
import logo from "../../public/assets/logo.png";

const Footer = () => {
  return (
    <footer className="border-t border-gray-200 dark:border-gray-800">
      <div className="max-w-[1440px] mx-auto px-4 sm:px-8 py-5 lg:py-3 flex flex-col lg:flex-row items-center justify-between gap-3 text-center">
        <div className="flex flex-col items-center lg:items-start">
          <Link href="/" className="flex items-center">
            <Image src={logo} alt="Blogout Logo" width={70} height={70} />
            <span className="font-semibold text-xl text-primary">Blogout</span>
          </Link>
        </div>

        <nav className="flex justify-center gap-4 lg:gap-5 text-sm text-primary dark:text-gray-400">
          <Link
            href="/about"
            className="hover:text-middle transition text-base"
          >
            About
          </Link>
          <Link
            href="/privacy-policy"
            className="hover:text-middle transition text-base"
          >
            Privacy Policy
          </Link>
        </nav>

        <div className="flex flex-col-reverse lg:flex-row items-center lg:items-end gap-3">
          <p className="text-base text-primary dark:text-primary">
            © {new Date().getFullYear()} Blogout. All rights reserved.
          </p>
          <div className="flex gap-3 text-xl text-primary dark:text-gray-400">
            <Link
              href="https://www.linkedin.com/in/m-abdullah-nadeem/"
              target="_blank"
              className="text-middle transition"
            >
              <FaLinkedin size={24} />
            </Link>
            <Link
              href="https://www.instagram.com/i_abdullahn/"
              target="_blank"
              className="text-middle transition"
            >
              <FaInstagram size={24} />
            </Link>
            <Link
              href="mailto:myselfabdullah360@gmail.com"
              className="text-middle transition"
            >
              <FaEnvelope size={24} />
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
