// Import necessary utilities from Vitest and Vue Test Utils
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { mount } from '@vue/test-utils';
import Friends from '@/components/Friends.vue'; // Adjust path as necessary

// Mock the '@/api/friends' module
vi.mock('@/api/friends', () => ({
  fetchFriends: vi.fn(() => Promise.resolve([{ friend: { username: 'john_doe', first_name: 'John', profile: { picture: 'path/to/image' } } }])),
  sendFriendRequest: vi.fn(),
  acceptFriendRequest: vi.fn(),
  rejectFriendRequest: vi.fn(),
  fetchFriendRequests: vi.fn(() => Promise.resolve([])),
  removeFriend: vi.fn(),
}));

describe('Friends.vue', () => {
  let wrapper;

  beforeEach(() => {
    // Mount the component before each test
    wrapper = mount(Friends, {
      global: {
        stubs: {
          // Stub out any child components that are not relevant to the test
          Navbar: true,
          CustomFooter: true,
        },
      },
    });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('loads friends on component mount', async () => {
    // Assuming fetchFriends is called on mounted
    // Wait for the next tick to allow the promise to resolve
    await wrapper.vm.$nextTick();

    // Assert that the friends list has been populated
    expect(wrapper.vm.friendsList).toHaveLength(1);
    expect(wrapper.vm.friendsList[0].friend.username).toBe('john_doe');

    // Optionally, assert DOM changes if necessary
    const friends = wrapper.findAll('.friend-card');
    expect(friends).toHaveLength(1);
  });

  // Additional tests here for other interactions
});
