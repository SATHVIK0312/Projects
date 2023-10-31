module.exports = {
  transform: {
    "^.+\\.jsx?$": "babel-jest",
    //".+\\.(css|styl|less|sass|scss)$": "jest-transform-css",
    "^.+\\.js$": "babel-jest"  // Add this line
  },
  // ... other configurations
};
