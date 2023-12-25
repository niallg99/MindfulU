import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import Registration from '@/components/Registration.vue';
import { registerUser } from '@/api/registration';
import loginApi from '@/api/login';
import { nextTick } from 'vue';

vi.mock('@/api/registration', () => ({
  registerUser: vi.fn(),
}));

vi.mock('@/api/login', () => ({
  getCSRFToken: vi.fn(),
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
    // Mock the API responses
    loginApi.getCSRFToken.mockResolvedValue('csrf_token_value');
    registerUser.mockResolvedValue({ success: true });

    // Fill out the registration form
    await wrapper.find('input[type="text"]#first_name').setValue('John');
    await wrapper.find('input[type="text"]#last_name').setValue('Doe');
    await wrapper.find('input[type="text"]#username').setValue('johndoe');
    await wrapper.find('input[type="tel"]#phone').setValue('123-456-7890');
    await wrapper.find('input[type="email"]#email').setValue('johndoe@gmail.com');
    await wrapper.find('input[type="password"]#password').setValue('password');

    // Submit the form
    await wrapper.find('form').trigger('submit.prevent');

    await nextTick();

    // Verify that the API was called
    expect(registerUser).toHaveBeenCalledWith({
      username: 'johndoe',
      phone: '123-456-7890',
      email: 'johndoe@gmail.com',
      password: 'password',
      first_name: 'John',
      last_name: 'Doe',
    }, 'csrf_token_value');

    // Verify navigation to login page
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/login');
  });

  it('displays error message on registration failure', async () => {
    // Mock the API responses
    loginApi.getCSRFToken.mockResolvedValue('csrf_token_value');
    registerUser.mockRejectedValue(new Error('Registration failed'));


    await nextTick();

    // Verify that the error message is displayed
    expect(wrapper.text()).toContain('Registration failed');
  });

  it('shows registration in progress', async () => {
    // Simulate that registration is in progress
    await wrapper.setData({ isRegistering: true });

    // Verify the button is disabled and the text "Registering..." is displayed
    const button = wrapper.find('button[type="submit"]');
    expect(button.attributes('disabled')).toBeDefined();
    expect(wrapper.text()).toContain('Registering...');
  });

});
