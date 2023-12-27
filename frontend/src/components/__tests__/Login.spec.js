// src/__tests__/Login.spec.js
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import Login from '@/components/Login.vue';
import loginApi from '@/api/login';
import { nextTick } from 'vue';

// Mocking the loginApi module and jwt-decode function
vi.mock('@/api/login', () => ({
  getCSRFToken: vi.fn(),
  loginUser: vi.fn(),
  verifyUserDetails: vi.fn(),
  resetUserPassword: vi.fn(),
}));
vi.mock('jwt-decode', () => vi.fn(() => ({ user_id: '123' })));

describe('Login.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(Login, {
      global: {
        stubs: {
          Navbar: true,
          'router-link': true,
          'custom-footer': true
        },
        mocks: {
          $router: {
            push: vi.fn(),
          },
        },
      },
    });
  });

  it('renders login form', () => {
    expect(wrapper.find('form').exists()).toBe(true);
    expect(wrapper.find('input[type="text"]').exists()).toBe(true);
    expect(wrapper.find('input[type="password"]').exists()).toBe(true);
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true);
  });

  it('submits the form and calls login method', async () => {
    // Mock the loginApi responses
    loginApi.getCSRFToken.mockResolvedValue('csrf_token_value');
    loginApi.loginUser.mockResolvedValue({ access_token: 'access_token_value' });

    await wrapper.find('input[type="text"]').setValue('user');
    await wrapper.find('input[type="password"]').setValue('password');
    await wrapper.find('form').trigger('submit.prevent');

    await nextTick();

    expect(loginApi.getCSRFToken).toHaveBeenCalled();
    expect(loginApi.loginUser).toHaveBeenCalled();
    // Add more assertions to check if the localStorage was set correctly
  });

  // ...previous tests...

it('sets the correct items in localStorage after a successful login', async () => {
  // Given
  const expectedUserId = '123';
  loginApi.getCSRFToken.mockResolvedValue('csrf_token_value');
  loginApi.loginUser.mockResolvedValue({ access_token: 'access_token_value' });
  const setItemMock = vi.spyOn(Storage.prototype, 'setItem');

  // When
  await wrapper.find('input[type="text"]').setValue('user');
  await wrapper.find('input[type="password"]').setValue('password');
  await wrapper.find('form').trigger('submit.prevent');

  await nextTick(); // Wait until the DOM updates.

  // Then
  expect(setItemMock).toHaveBeenCalledWith('accessToken', 'access_token_value');
  expect(setItemMock).toHaveBeenCalledWith('userId', expectedUserId);
  expect(setItemMock).toHaveBeenCalledWith('username', 'user');
  expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/dashboard');

  // Cleanup
  setItemMock.mockRestore();
});

it('displays an error message when login fails', async () => {
  // Given
  loginApi.getCSRFToken.mockResolvedValue('csrf_token_value');
  loginApi.loginUser.mockRejectedValue(new Error('Invalid credentials'));

  // When
  await wrapper.find('input[type="text"]').setValue('user');
  await wrapper.find('input[type="password"]').setValue('wrong_password');
  await wrapper.find('form').trigger('submit.prevent');

  await nextTick(); // Wait for the DOM to update

  // Then
  expect(wrapper.text()).toContain('Invalid credentials');
});

it('verifies user details correctly', async () => {
  // Given
  loginApi.verifyUserDetails.mockResolvedValue({ verified: true });

  // When
  await wrapper.setData({ email: 'user@example.com' });
  await wrapper.find('form').trigger('submit.prevent'); // Assuming this triggers verifyDetails

  await nextTick(); // Wait for the DOM to update

  // Then
  expect(wrapper.vm.verifyStage).toBe(true);
  expect(loginApi.verifyUserDetails).toHaveBeenCalledWith({ email: 'user@example.com' });
});

it('handles verification failure correctly', async () => {
  // Given
  loginApi.verifyUserDetails.mockRejectedValue(new Error('Verification failed: Incorrect details'));

  // When
  await wrapper.setData({ email: 'incorrect@example.com' });
  await wrapper.find('form').trigger('submit.prevent'); // Assuming this triggers verifyDetails

  await nextTick(); // Wait for the DOM to update

  // Then
  expect(wrapper.vm.verifyStage).toBe(false);
  expect(wrapper.vm.errorMessage).toBe('Verification failed: Incorrect details');
});

it('resets password correctly', async () => {
  // Given
  loginApi.resetUserPassword.mockResolvedValue({});
  wrapper.vm.verifyStage = true; // Mock that the user has been verified already.

  // When
  await wrapper.setData({ newPassword: 'newpassword' });
  await wrapper.find('form').trigger('submit.prevent'); // Assuming this triggers resetPassword

  await nextTick(); // Wait for the DOM to update

  // Then
  expect(wrapper.vm.verifyStage).toBe(false);
  expect(loginApi.resetUserPassword).toHaveBeenCalledWith('user@example.com', 'newpassword');
  // You would also check for the modal closure and reset of fields if applicable
});
});
