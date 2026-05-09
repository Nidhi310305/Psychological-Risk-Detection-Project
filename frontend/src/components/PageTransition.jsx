import React from 'react';

const PageTransition = ({ children }) => {
  return <div className="page-container animate-fade-in">{children}</div>;
};

export default PageTransition;
