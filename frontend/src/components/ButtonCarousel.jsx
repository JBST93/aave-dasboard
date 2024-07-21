import React, { useState, useRef } from 'react';
import FilterButton from './FilterButton';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa';

const ButtonCarousel = ({ onClick }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isSwiping, setIsSwiping] = useState(false);
  const touchStartXRef = useRef(0);
  const carouselRef = useRef(null);

  const items = [
    { token: '', label: 'ALL' },
    { token: 'USDC', label: 'USDC' },
    { token: 'USDT', label: 'USDT' },
    { token: 'DAI', label: 'DAI' },
  ];

  const updateCarousel = (index) => {
    if (carouselRef.current) {
      const itemWidth = carouselRef.current.children[0].clientWidth;
      carouselRef.current.style.transform = `translateX(${
        -index * itemWidth
      }px)`;
    }
  };

  const handleNext = () => {
    if (currentIndex < items.length - 1) {
      setCurrentIndex((prevIndex) => {
        const newIndex = prevIndex + 1;
        updateCarousel(newIndex);
        return newIndex;
      });
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prevIndex) => {
        const newIndex = prevIndex - 1;
        updateCarousel(newIndex);
        return newIndex;
      });
    }
  };

  const handleTouchStart = (e) => {
    setIsSwiping(true);
    touchStartXRef.current = e.touches[0].clientX;
  };

  const handleTouchMove = (e) => {
    if (!isSwiping) return;

    const touchEndX = e.touches[0].clientX;
    const touchDiff = touchStartXRef.current - touchEndX;

    if (touchDiff > 50) {
      handleNext();
      setIsSwiping(false);
    } else if (touchDiff < -50) {
      handlePrev();
      setIsSwiping(false);
    }
  };

  const handleTouchEnd = () => {
    setIsSwiping(false);
  };

  return (
    <div className="relative flex items-center w-full max-w-lg mx-auto">
      <button
        onClick={handlePrev}
        className="absolute left-0 z-10  text-basefocus:outline-none"
        style={{ transform: 'translateX(-50%)' }}
      >
        <FaChevronLeft className="w-6 h-6 text-gray-700 dark:text-gray-300" />
      </button>
      <div
        className="w-full overflow-hidden"
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        <div
          className="flex transition-transform duration-500 ease"
          ref={carouselRef}
        >
          {items.map((item, index) => (
            <FilterButton
              key={index}
              token={item.token}
              onClick={onClick}
              label={item.label}
              className="flex-shrink-0 p-1"
            />
          ))}
        </div>
      </div>
      <button
        onClick={handleNext}
        className="absolute right-0 z-10 p-2 text-base  focus:outline-none"
        style={{ transform: 'translateX(50%)' }}
      >
        <FaChevronRight className="w-6 h-6 text-gray-700 dark:text-gray-300" />
      </button>
    </div>
  );
};

export default ButtonCarousel;
