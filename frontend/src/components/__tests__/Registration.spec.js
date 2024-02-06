import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import Registration from '@/components/Registration.vue';
import { registerUser } from '@/api/registration';

vi.mock('@/api/registration', () => ({
  registerUser: vi.fn(() => Promise.resolve({ success: true })),
}));

vi.mock('@/api/login', () => ({
  default: {
    getCSRFToken: vi.fn(() => Promise.resolve('csrf_token_value')),
  },
}));

describe('Registration.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(Registration, {
      global: {
        stubs: {
          'router-link': true,
        },
        mocks: {
          $router: {
            push: vi.fn(),
          },
        },
      },
    });
  });

  it('renders registration form', () => {
    expect(wrapper.find('form').exists()).toBe(true);
    expect(wrapper.find('input[type="text"]').exists()).toBe(true);
    expect(wrapper.find('input[type="password"]').exists()).toBe(true);
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true);
  });

  it('registers a user successfully', async () => {
    // Set input values
    await wrapper.find('input[type="text"]#first_name').setValue('John');
    await wrapper.find('input[type="text"]#last_name').setValue('Doe');
    await wrapper.find('input[type="text"]#username').setValue('johndoe');
    await wrapper.find('input[type="tel"]#phone').setValue('123-456-7890');
    await wrapper.find('input[type="email"]#email').setValue('johndoe@gmail.com');
    await wrapper.find('input[type="password"]#password').setValue('password');

    // Submit the form
    await wrapper.find('form').trigger('submit.prevent');

    // Wait for any nextTicks and promises to resolve
    await flushPromises();

    // Assert navigation to the login page
    expect(wrapper.vm.$router.push).toHaveBeenCalledTimes(1);
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/login');
  });

  it('displays error message on registration failure', async () => {
    // Mock a rejected promise for registerUser with a message
    registerUser.mockRejectedValueOnce(new Error('Registration failed'));

    // Attempt to submit the form without setting input values
    await wrapper.find('form').trigger('submit.prevent');
    
    // Wait for any nextTicks and promises to resolve
    await flushPromises();

    // Assert the error message is displayed
    expect(wrapper.vm.errorMessage).toBe('Registration failed');
  });

  it('shows registration in progress', async () => {
    // Simulate that registration is in progress
    wrapper.vm.isRegistering = true;

    // Wait for the Vue instance to update
    await flushPromises();

    // Assert the button is disabled and the text "Registering..." is displayed
    const button = wrapper.find('button[type="submit"]');
    expect(button.attributes('disabled')).toBeDefined();
  });

  // Add more tests as needed
});
