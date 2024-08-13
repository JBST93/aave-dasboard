import React from 'react';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';

const Blog = () => {
  const posts = [
    {
      title: 'Stablecoin Yield Farming: A Complete Guide',
      excerpt:
        'Learn how to earn passive income through stablecoin yield farming using USDC, USDT, and DAI on top DeFi platforms.',
      link: '/blog/stablecoin-yield-farming',
      date: 'August 13, 2024',
    },
  ];

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <Helmet>
        <title>Our Blog | Token Data View</title>
        <meta
          name="description"
          content="Explore our blog for the latest insights on DeFi, stablecoin yield farming, and more. Stay informed with our in-depth guides and articles."
        />
      </Helmet>

      <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">
        Token Data View Blog: Your Guide to DeFi & Yield Farming
      </h1>
      <p className="text-lg text-gray-700  dark:text-white mb-8">
        Welcome to our blog! Here you can find the latest articles, guides, and
        insights on decentralized finance (DeFi), stablecoins, and yield
        farming. Click on any post to read more.
      </p>

      <div className="space-y-8">
        {posts.map((post, index) => (
          <div
            key={index}
            className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200"
          >
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">
              <Link
                to={post.link}
                className="hover:text-blue-500"
              >
                {post.title}
              </Link>
            </h2>
            <p className="text-gray-600 mb-4">{post.excerpt}</p>
            <p className="text-sm text-gray-500">{post.date}</p>
            <Link
              to={post.link}
              className="text-blue-500 hover:text-blue-700"
            >
              Read more →
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Blog;
