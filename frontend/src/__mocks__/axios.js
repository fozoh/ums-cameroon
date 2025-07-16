// __mocks__/axios.js
export default {
  post: jest.fn(() => Promise.resolve({ data: {} })),
  get: jest.fn(() => Promise.resolve({ data: {} })),
  // Add other methods as needed
};
