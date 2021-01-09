import authorizationService from '@/services/authorization.service'

export default {
    methods: {
        isAuthenticated: function () {
            return authorizationService.isAuthenticated()
        },
    }
}