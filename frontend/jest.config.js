module.exports = {
  transform: {
    '^.+\\.[jt]sx?$': 'babel-jest',
  },
  testEnvironment: 'jsdom',
  moduleFileExtensions: ['js', 'jsx', 'json', 'node'],
  transformIgnorePatterns: [
    '/node_modules/(?!(axios)/)',
  ],
};
