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
        <title>
          {' '}
          Blog: Your Guide to DeFi & Yield Farming | Token Data View
        </title>
        <meta
          name="description"
          content="Explore our blog for the latest insights on DeFi, stablecoin yield farming, and more. Stay informed with our in-depth guides and articles."
        />
        <meta
          name="keywords"
          content="DeFi, Yield Farming, Stablecoin, Cryptocurrency, Blockchain, Token Data View, Guides, Articles"
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
            className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200"
          >
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
              <Link
                to={post.link}
                className="hover:text-blue-500"
              >
                {post.title}
              </Link>
            </h2>
            <p className="text-sm text-gray-500 flex">{post.date}</p>

            <p className="text-gray-600 dark:text-gray-200 mb-4">
              {post.excerpt}
            </p>

            <Link
              to={post.link}
              className="text-blue-500 hover:text-blue-700 flex mt-2"
            >
              <div className="border border-yellow-500 dark:border-teal-700 text-black dark:text-white px-3 py-2">
                Read more →
              </div>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Blog;
