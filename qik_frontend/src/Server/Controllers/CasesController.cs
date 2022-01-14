using backend.Services;
using backend.Models;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;

namespace backend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CasesController : ControllerBase
    {
        private readonly CasesService _casesService;

        public CasesController(CasesService casesService)
        {
            _casesService = casesService;
        }

        [HttpGet]
        public ActionResult<List<dynamic>> Get() =>
            _casesService.Get();

        [HttpPost("SearchCase")]
        public ActionResult<List<Cases>> SearchCase(string option, string query) {
            if(option == "All"){
               return  _casesService.SearchAllCases(query);
            }
            else if(option == "Case ID"){
                return _casesService.SearchCaseID(query);
            }
            else if(option == "Case Name"){
                return _casesService.SearchCaseName(query);
            }
            else if(option == "Case Description"){
                return _casesService.SearchCaseDescription(query);
            }
            else if(option == "Crime Type"){
                return _casesService.SearchCaseType(query);
            }
            else if(option == "Status"){
                return _casesService.SearchCaseStatus(query);
            }
            else if(option == "Creator"){
                return _casesService.SearchCaseCreator(query);
            }
            else if(option == "Assignee"){
                return _casesService.SearchCaseAssignee(query);
            }
            else if(option == "Priority"){
                return _casesService.SearchCasePriority(query);
            }
            
            return new List<Cases>();
        }
    }
}