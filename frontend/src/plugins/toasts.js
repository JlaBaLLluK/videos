import {toast} from 'bulma-toast';

export function errorToast(message) {
  toast({
    type: 'is-danger',
    position: 'top-center',
    message: message,
    duration: 3000,
  });
}

export function infoToast(message) {
  toast({
    type: 'is-info',
    position: 'top-center',
    message: message,
    duration: 3000,
  });
}

export function successToast(message) {
  toast({
    type: 'is-success',
    position: 'top-center',
    message: message,
    duration: 3000
  });
}
